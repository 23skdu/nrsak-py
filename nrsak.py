#!/usr/bin/env python3
"""New Relic Swiss Army Knife (nrsak)."""

import argparse
import inspect
import json
import os
import sys

import requests

NR_API = "https://api.newrelic.com/v2/"
NR_NERDGRAPH = "https://api.newrelic.com/graphql"
REQUEST_TIMEOUT = 30


def _api_key():
    key = os.environ.get("NR_KEY")
    if not key:
        print("you must have NR_KEY environment variable set")
        sys.exit(1)
    return key


def _url(path):
    if str(path).startswith("http://") or str(path).startswith("https://"):
        return str(path)
    return NR_API + str(path).lstrip("/")


def _get(path, params=None):
    response = requests.get(
        _url(path),
        headers={"Api-Key": _api_key(), "Accept": "application/json"},
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    try:
        data = response.json()
    except ValueError:
        data = response.text
    print(response.text)
    return data


def _post(path, json=None, params=None):
    response = requests.post(
        _url(path),
        headers={
            "Api-Key": _api_key(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json=json,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    try:
        data = response.json()
    except ValueError:
        data = response.text
    print(response.text)
    return data


def _graphql(query, variables=None):
    response = requests.post(
        NR_NERDGRAPH,
        headers={
            "Api-Key": _api_key(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={"query": query, "variables": variables or {}},
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        print(f"Error: {response.status_code}")
        print(response.text)
        sys.exit(1)
    try:
        payload = response.json()
    except ValueError:
        print(response.text)
        sys.exit(1)
    if payload.get("errors"):
        print(json.dumps(payload["errors"]))
        sys.exit(1)
    print(response.text)
    return payload.get("data")


def _env(name, default=None):
    return os.environ.get(name, default)


def _require(value, message):
    if not value:
        print(message)
        sys.exit(1)
    return value


def nrSummary():
    """List all APM applications."""
    return _get("applications.json")


def nrApplications():
    """Alias for nrSummary."""
    return _get("applications.json")


def nrApplication(app_id=None):
    """Get a single application by id (or list all when no id is given)."""
    app_id = app_id if app_id is not None else _env("APP_ID")
    if not app_id:
        return nrApplications()
    return _get(f"applications/{app_id}.json")


def nrMetrics(app_id=None):
    """List available metrics for an application."""
    app_id = _require(app_id if app_id is not None else _env("APP_ID"), "APP_ID is required")
    return _get(f"applications/{app_id}/metrics.json")


def nrServers():
    """List all servers."""
    return _get("servers.json")


def nrServer(server_id=None):
    """Get a single server by id (or list all when no id is given)."""
    server_id = server_id if server_id is not None else _env("SERVER_ID")
    if not server_id:
        return nrServers()
    return _get(f"servers/{server_id}.json")


def nrAlertPolicies():
    """List alert policies."""
    return _get("alerts_policies.json")


def nrAlertConditions(policy_id=None):
    """List alert conditions, optionally filtered by policy id."""
    policy_id = policy_id if policy_id is not None else _env("POLICY_ID")
    params = {"policy_id": policy_id} if policy_id else None
    return _get("alerts_conditions.json", params=params)


def nrAlertViolations():
    """List recent alert violations."""
    return _get("alerts_violations.json")


def nrAlertIncidents():
    """List recent alert incidents."""
    return _get("alerts_incidents.json")


def nrDeployments(app_id=None):
    """List deployments for an application."""
    app_id = _require(app_id if app_id is not None else _env("APP_ID"), "APP_ID is required")
    return _get(f"applications/{app_id}/deployments.json")


def nrCreateDeployment(app_id=None, revision=None, changelog=None, description=None, user=None):
    """Create a deployment marker for an application."""
    app_id = _require(app_id if app_id is not None else _env("APP_ID"), "APP_ID is required")
    revision = revision if revision is not None else _env("REVISION")
    _require(revision, "revision is required")
    deployment = {"revision": revision}
    if changelog is not None or _env("CHANGELOG"):
        deployment["changelog"] = changelog if changelog is not None else _env("CHANGELOG")
    if description is not None or _env("DESCRIPTION"):
        deployment["description"] = description if description is not None else _env("DESCRIPTION")
    if user is not None or _env("DEPLOY_USER"):
        deployment["user"] = user if user is not None else _env("DEPLOY_USER")
    return _post(f"applications/{app_id}/deployments.json", json={"deployment": deployment})


def nrPlugins():
    """List installed plugins."""
    return _get("plugins.json")


def nrLabels():
    """List labels."""
    return _get("labels.json")


def nrKeyTransactions():
    """List key transactions."""
    return _get("key_transactions.json")


def nrSyntheticMonitors():
    """List Synthetics monitors."""
    return _get("https://synthetics.newrelic.com/synthetics/api/v3/monitors")


def nrAccount():
    """Return the accounts available to the API key."""
    return _graphql("{ actor { accounts { id name } } }")


def nrAccounts():
    """Alias for nrAccount."""
    return _graphql("{ actor { accounts { id name } } }")


def nrUser():
    """Return information about the current user."""
    return _graphql("{ actor { user { id name email } } }")


def nrNrql(query=None, account_id=None):
    """Run a NRQL query through NerdGraph."""
    query = (
        query
        if query is not None
        else (_env("NRQL") or "SELECT count(*) FROM Transaction SINCE 1 hour ago")
    )
    account_id = account_id if account_id is not None else _env("NR_ACCOUNT_ID")
    _require(account_id, "NR_ACCOUNT_ID is required")
    gql = """
    query($accountId: Int!, $nrql: Nrql!) {
      actor {
        account(id: $accountId) {
          nrql(query: $nrql) { results }
        }
      }
    }
    """
    return _graphql(gql, {"accountId": int(account_id), "nrql": query})


def nrEntities(query=None):
    """Search entities through NerdGraph."""
    query = query if query is not None else (_env("ENTITY_QUERY") or "name LIKE '%'")
    gql = """
    query($q: String!) {
      actor {
        entitySearch(query: $q) {
          results {
            entities { guid name type entityType domain }
          }
        }
      }
    }
    """
    return _graphql(gql, {"q": query})


def nrWorkloads():
    """List workloads through NerdGraph."""
    gql = "{ actor { workloads { search { results { guid name } } } } }"
    return _graphql(gql)


def nrDashboards():
    """List dashboards through NerdGraph."""
    gql = "{ actor { dashboards { search { dashboards { guid name } } } } }"
    return _graphql(gql)


def function_list(module=None):
    """Print (and return) all nr* functions defined in a module."""
    mod = module if module is not None else sys.modules[__name__]
    names = []
    for name, obj in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith("nr"):
            print(name)
            names.append(name)
    return names


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nrsak", description="New Relic Swiss Army Knife")
    parser.add_argument("action", nargs="?", help="function name to invoke")
    parser.add_argument("rest", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if not args.action:
        parser.print_help()
        return 0

    if args.action == "function_list":
        function_list()
        return 0

    func = globals().get(args.action)
    if not callable(func):
        print(f"unknown action: {args.action}")
        return 2

    try:
        func()
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
