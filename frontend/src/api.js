const API_BASE = "http://127.0.0.1:8000/api/game";

async function handle(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

export function newGame() {
  return fetch(`${API_BASE}/new`, { method: "POST" }).then(handle);
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

export function pass(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/pass`, { method: "POST" }).then(handle);
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

export function getRemainingPlayers(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/players/remaining`).then(handle);
}

export function completeSimulation(sessionId) {
  return fetch(`${API_BASE}/${sessionId}/complete-simulation`, { method: "POST" }).then(handle);
}
