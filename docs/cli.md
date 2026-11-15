# nrsak CLI reference

`nrsak` is a small command line tool around the New Relic REST and NerdGraph
APIs. It requires the `NR_KEY` environment variable to be set to a New Relic
API key.

## Usage

```bash
NR_KEY=your-key python3 nrsak.py <action>
```

In Docker:

```bash
docker run --rm -e NR_KEY=your-key nrsak-py:latest <action>
```

Run `function_list` (the default container command) to print every available
`nr*` action:

```bash
python3 nrsak.py function_list
```

## Environment variables

| Variable | Used by | Description |
| --- | --- | --- |
| `NR_KEY` | all | New Relic API key (required) |
| `APP_ID` | `nrApplication`, `nrMetrics`, `nrDeployments`, `nrCreateDeployment` | APM application id |
| `SERVER_ID` | `nrServer` | Server id |
| `POLICY_ID` | `nrAlertConditions` | Alert policy id |
| `NR_ACCOUNT_ID` | `nrNrql` | New Relic account id (integer) |
| `NRQL` | `nrNrql` | NRQL query string |
| `ENTITY_QUERY` | `nrEntities` | NerdGraph entity search query |
| `REVISION` | `nrCreateDeployment` | Deployment revision |
| `CHANGELOG` | `nrCreateDeployment` | Deployment changelog |
| `DESCRIPTION` | `nrCreateDeployment` | Deployment description |
| `DEPLOY_USER` | `nrCreateDeployment` | Deploying user |

## Actions

### Applications / APM

- `nrSummary` / `nrApplications` - list all APM applications.
- `nrApplication [app_id]` - get a single application (`APP_ID` env if omitted).
- `nrMetrics` - list available metrics for an application (`APP_ID`).

### Servers

- `nrServers` - list all servers.
- `nrServer` - get a single server (`SERVER_ID`).

### Alerts

- `nrAlertPolicies` - list alert policies.
- `nrAlertConditions` - list alert conditions (`POLICY_ID` optional).
- `nrAlertViolations` - list recent alert violations.
- `nrAlertIncidents` - list recent alert incidents.

### Deployments

- `nrDeployments` - list deployments for an application (`APP_ID`).
- `nrCreateDeployment` - create a deployment marker (`APP_ID`, `REVISION`, ...).

### Plugins, labels, key transactions

- `nrPlugins` - list installed plugins.
- `nrLabels` - list labels.
- `nrKeyTransactions` - list key transactions.

### Synthetics

- `nrSyntheticMonitors` - list Synthetics monitors.

### NerdGraph

- `nrAccount` / `nrAccounts` - list accounts.
- `nrUser` - current user info.
- `nrNrql` - run a NRQL query (`NR_ACCOUNT_ID`, `NRQL`).
- `nrEntities` - search entities (`ENTITY_QUERY`).
- `nrWorkloads` - list workloads.
- `nrDashboards` - list dashboards.

### Introspection

- `function_list` - print all available `nr*` actions.
