const ROOT = "http://127.0.0.1:8000/api";
const API_BASE = `${ROOT}/game`;
const PLAYERS_BASE = `${ROOT}/players`;

async function handle(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

export function generatePool({ seed, count } = {}) {
  const body = {};
  if (seed !== undefined && seed !== null && seed !== "") body.seed = Number(seed);
  if (count !== undefined && count !== null && count !== "") body.count = Number(count);
  const hasBody = Object.keys(body).length > 0;
  return fetch(`${PLAYERS_BASE}/generate`, {
    method: "POST",
    headers: hasBody ? { "Content-Type": "application/json" } : undefined,
    body: hasBody ? JSON.stringify(body) : undefined,
  }).then(handle);
}

export function getPoolSummary(poolId) {
  return fetch(`${PLAYERS_BASE}/${poolId}/summary`).then(handle);
}

export function getPoolPlayers(poolId) {
  return fetch(`${PLAYERS_BASE}/${poolId}/players`).then(handle);
}

export function getPlayerDetail(poolId, playerId) {
  return fetch(`${PLAYERS_BASE}/${poolId}/players/${playerId}/detail`).then(handle);
}

export function getWeightTables() {
  return fetch(`${PLAYERS_BASE}/weight-tables`).then(handle);
}

export function previewCustomPlayer(body) {
  return fetch(`${PLAYERS_BASE}/preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then(handle);
}

export function createCustomPlayer(poolId, body) {
  return fetch(`${PLAYERS_BASE}/${poolId}/custom`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then(handle);
}

export function newGame(poolId) {
  return fetch(`${API_BASE}/new`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pool_id: poolId }),
  }).then(handle);
}

export function getGame(sessionId) {
  return fetch(`${API_BASE}/${sessionId}`).then(handle);
}

export function bid(sessionId, increment) {
  return fetch(`${API_BASE}/${sessionId}/bid`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ increment }),
  }).then(handle);
}

export function skip(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/skip`, { method: "POST" }).then(handle);
}

export function advance(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/advance`, { method: "POST" }).then(handle);
}

export function pause(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/pause`, { method: "POST" }).then(handle);
}

export function resume(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/resume`, { method: "POST" }).then(handle);
}

export function getTeam(sessionId, teamKey) {
  return fetch(`${API_BASE}/${sessionId}/teams/${teamKey}`).then(handle);
}

export function getStartingEleven(sessionId, teamKey) {
  return fetch(`${API_BASE}/${sessionId}/teams/${teamKey}/starting-eleven`).then(handle);
}

export function getSummary(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/summary`).then(handle);
}

export function getRemainingPlayers(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/players/remaining`).then(handle);
}

export function completeSimulation(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/complete-simulation`, { method: "POST" }).then(handle);
}
