
import pytest

import nrsak


@pytest.fixture(autouse=True)
def env_key(monkeypatch):
    monkeypatch.setenv("NR_KEY", "test-key")
    yield


def test_function_list_returns_nr_functions():
    names = nrsak.function_list(nrsak)
    assert "nrSummary" in names
    assert "nrServers" in names
    assert all(n.startswith("nr") for n in names)


def test_function_list_prints(capsys):
    nrsak.function_list(nrsak)
    out = capsys.readouterr().out
    assert "nrSummary" in out


def test_nr_summary_success(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/applications.json", json={"applications": [{"name": "A"}]})
    result = nrsak.nrSummary()
    assert result == {"applications": [{"name": "A"}]}


def test_nr_summary_missing_key(monkeypatch):
    monkeypatch.delenv("NR_KEY", raising=False)
    with pytest.raises(SystemExit):
        nrsak.nrSummary()


def test_nr_summary_error_status(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/applications.json", status_code=401, text="unauthorized")
    with pytest.raises(SystemExit):
        nrsak.nrSummary()


def test_nr_application_by_id(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/applications/42.json", json={"application": {"id": 42}})
    result = nrsak.nrApplication(42)
    assert result == {"application": {"id": 42}}


def test_nr_application_none_lists_all(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/applications.json", json={"applications": []})
    result = nrsak.nrApplication(None)
    assert result == {"applications": []}


def test_nr_servers(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/servers.json", json={"servers": []})
    assert nrsak.nrServers() == {"servers": []}


def test_nr_alert_policies(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/alerts_policies.json", json={"policies": []})
    assert nrsak.nrAlertPolicies() == {"policies": []}


def test_nr_alert_conditions_with_policy(requests_mock):
    requests_mock.get("https://api.newrelic.com/v2/alerts_conditions.json", json={"conditions": []})
    nrsak.nrAlertConditions(7)
    assert requests_mock.last_request.qs.get("policy_id") == ["7"]


def test_nr_deployments_requires_app_id(monkeypatch):
    monkeypatch.delenv("APP_ID", raising=False)
    with pytest.raises(SystemExit):
        nrsak.nrDeployments()


def test_nr_create_deployment(requests_mock, monkeypatch):
    monkeypatch.setenv("APP_ID", "5")
    requests_mock.post("https://api.newrelic.com/v2/applications/5/deployments.json", json={"deployment": {"id": 1}})
    result = nrsak.nrCreateDeployment(revision="v1.2.3", changelog="changes")
    assert result == {"deployment": {"id": 1}}
    assert requests_mock.last_request.json()["deployment"]["revision"] == "v1.2.3"


def test_nr_nrql(requests_mock, monkeypatch):
    monkeypatch.setenv("NR_ACCOUNT_ID", "12345")
    requests_mock.post("https://api.newrelic.com/graphql", json={"data": {"actor": {"account": {"nrql": {"results": [{"count": 1}]}}}}})
    result = nrsak.nrNrql("SELECT count(*) FROM Transaction SINCE 1 hour ago", account_id=12345)
    assert result["actor"]["account"]["nrql"]["results"] == [{"count": 1}]


def test_nr_nrql_missing_account():
    with pytest.raises(SystemExit):
        nrsak.nrNrql(account_id=None)


def test_nr_account(requests_mock):
    requests_mock.post("https://api.newrelic.com/graphql", json={"data": {"actor": {"accounts": [{"id": 1, "name": "Acct"}]}}})
    result = nrsak.nrAccount()
    assert result["actor"]["accounts"][0]["name"] == "Acct"


def test_nr_entities(requests_mock):
    requests_mock.post("https://api.newrelic.com/graphql", json={"data": {"actor": {"entitySearch": {"results": {"entities": [{"guid": "g"}]}}}}})
    result = nrsak.nrEntities("name LIKE '%foo%'")
    assert result["actor"]["entitySearch"]["results"]["entities"][0]["guid"] == "g"


def test_nr_graphql_error(requests_mock):
    requests_mock.post("https://api.newrelic.com/graphql", json={"errors": [{"message": "boom"}]}, status_code=200)
    with pytest.raises(SystemExit):
        nrsak.nrAccount()


def test_main_function_list(capsys):
    rc = nrsak.main(["function_list"])
    assert rc == 0
    assert "nrSummary" in capsys.readouterr().out


def test_main_unknown_action():
    assert nrsak.main(["doesNotExist"]) == 2


def test_main_no_action(capsys):
    rc = nrsak.main([])
    assert rc == 0


def test_main_missing_key_returns_code(monkeypatch):
    monkeypatch.delenv("NR_KEY", raising=False)
    rc = nrsak.main(["nrSummary"])
    assert rc == 1
