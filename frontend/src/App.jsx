import { useEffect, useRef, useState } from "react";
import * as api from "./api";
import "./App.css";

const POLL_MS = 1000;

function PlayerCard({ player }) {
  if (!player) return <div className="panel">No player on the block.</div>;
  return (
    <div className="panel">
      <h2>{player.name}</h2>
      <p>
        {player.position} · Est. value {player.estimated_price}
      </p>
      <ul className="stat-list">
        <li>Batting: {player.batting}</li>
        <li>Bowling: {player.bowling}</li>
        <li>Fielding: {player.fielding}</li>
        <li>Batting hand: {player.batting_hand}</li>
        <li>Batting order: {player.batting_order}</li>
        <li>Bowling type: {player.bowling_type}</li>
      </ul>
    </div>
  );
}

function AuctionStatus({ state, onShowRemainingPlayers }) {
  return (
    <div className="panel">
      <h3>Auction Status</h3>
      <p>Round {state.round_number}</p>
      <p>Phase: {state.phase.replace("_", " ")}</p>
      <p>Current price: {state.current_price}</p>
      <p>Leading bidder: {state.current_leader || "None yet"}</p>
      <p>
        Players remaining: {state.players_remaining}{" "}
        <button className="link-button" onClick={onShowRemainingPlayers}>
          [Show]
        </button>
      </p>
      {state.last_result && (
        <p className="last-result">
          {state.last_result.type === "sold"
            ? `SOLD: ${state.last_result.player_name} -> ${state.last_result.winner} for ${state.last_result.price}`
            : `UNSOLD: ${state.last_result.player_name}`}
        </p>
      )}
    </div>
  );
}

function Controls({ state, onBid, onPass, onSkip, onAdvance, busy }) {
  const [customAmount, setCustomAmount] = useState("");

  if (state.phase === "game_over") {
    return <div className="panel">Auction complete.</div>;
  }

  if (state.available_actions.includes("advance")) {
    return (
      <div className="panel">
        <button disabled={busy} onClick={onAdvance}>
          Continue
        </button>
      </div>
    );
  }

  return (
    <div className="panel">
      <h3>Your Move</h3>
      <div className="bid-buttons">
        {state.allowed_increments.map((amount) => (
          <button key={amount} disabled={busy} onClick={() => onBid(amount)}>
            +{amount}
          </button>
        ))}
      </div>
      <div className="custom-bid">
        <input
          type="number"
          min="1"
          placeholder="Custom amount"
          value={customAmount}
          onChange={(e) => setCustomAmount(e.target.value)}
        />
        <button
          disabled={busy || !customAmount}
          onClick={() => {
            onBid(Number(customAmount));
            setCustomAmount("");
          }}
        >
          Bid
        </button>
      </div>
      <div className="secondary-actions">
        <button disabled={busy} onClick={onPass} className="pass-button">
          Pass
        </button>
        <button disabled={busy} onClick={onSkip} className="skip-button" title="Resolve this player instantly, without watching the live clock">
          Skip &raquo;
        </button>
      </div>
    </div>
  );
}

function BidderSummary({ title, summary, onSelectTeam }) {
  return (
    <div className="panel">
      <h3>{title}</h3>
      <p>
        <button className="link-button" onClick={() => onSelectTeam(summary.key, summary)}>
          {summary.name}
        </button>
      </p>
      <p>Budget: {summary.budget}</p>
      <p>Squad size: {summary.squad_size}</p>
      {summary.composition && (
        <ul className="stat-list">
          <li>Batsmen: {summary.composition.batsmen}</li>
          <li>Bowlers: {summary.composition.bowlers}</li>
          <li>Allrounders: {summary.composition.allrounders}</li>
          <li>Wicketkeepers: {summary.composition.wicketkeepers}</li>
        </ul>
      )}
    </div>
  );
}

function RivalsPanel({ rivals, onSelectTeam }) {
  return (
    <div className="panel">
      <h3>Rival Teams</h3>
      <table>
        <thead>
          <tr>
            <th>Team</th>
            <th>Budget</th>
            <th>Squad</th>
          </tr>
        </thead>
        <tbody>
          {rivals.map((r) => (
            <tr key={r.key}>
              <td>
                <button className="link-button" onClick={() => onSelectTeam(r.key)}>
                  {r.name}
                </button>
              </td>
              <td>{r.budget}</td>
              <td>{r.squad_size}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SquadModal({ team, loading, error, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{team ? team.name : "Loading..."}</h2>
          <button onClick={onClose}>Close</button>
        </div>
        {loading && <p>Loading squad...</p>}
        {error && <p className="error-banner">{error}</p>}
        {team && (
          <>
            <p>
              Budget: {team.budget} · Squad size: {team.squad_size}
            </p>
            {team.composition && (
              <p>
                Batsmen: {team.composition.batsmen} · Bowlers: {team.composition.bowlers} ·
                Allrounders: {team.composition.allrounders} · Wicketkeepers:{" "}
                {team.composition.wicketkeepers}
              </p>
            )}
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Position</th>
                  <th>Batting</th>
                  <th>Bowling</th>
                  <th>Fielding</th>
                  <th>Price Paid</th>
                </tr>
              </thead>
              <tbody>
                {(team.squad || []).map((p) => (
                  <tr key={p.player_id}>
                    <td>{p.name}</td>
                    <td>{p.position}</td>
                    <td>{p.batting}</td>
                    <td>{p.bowling}</td>
                    <td>{p.fielding}</td>
                    <td>{p.selling_price ?? "-"}</td>
                  </tr>
                ))}
                {team.squad && team.squad.length === 0 && (
                  <tr>
                    <td colSpan="6">No players bought yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}

function PlayerListModal({ data, loading, error, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Remaining Players{data ? ` (${data.count})` : ""}</h2>
          <button onClick={onClose}>Close</button>
        </div>
        {loading && <p>Loading players...</p>}
        {error && <p className="error-banner">{error}</p>}
        {data && (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Batting</th>
                <th>Bowling</th>
                <th>Fielding</th>
                <th>Est. Value</th>
              </tr>
            </thead>
            <tbody>
              {data.players.map((p) => (
                <tr key={p.player_id}>
                  <td>{p.name}</td>
                  <td>{p.position}</td>
                  <td>{p.batting}</td>
                  <td>{p.bowling}</td>
                  <td>{p.fielding}</td>
                  <td>{p.estimated_price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function ActivityFeed({ events }) {
  const recent = [...events].reverse();
  return (
    <div className="panel activity-feed">
      <h3>Activity</h3>
      <ul>
        {recent.map((event, i) => (
          <li key={i}>{event}</li>
        ))}
      </ul>
    </div>
  );
}

export default function App() {
  const [state, setState] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teamLoading, setTeamLoading] = useState(false);
  const [teamError, setTeamError] = useState(null);
  const [remainingPlayers, setRemainingPlayers] = useState(null);
  const [remainingPlayersOpen, setRemainingPlayersOpen] = useState(false);
  const [remainingLoading, setRemainingLoading] = useState(false);
  const [remainingError, setRemainingError] = useState(null);

  // The auction now runs on its own clock server-side (see live_clock.py) -
  // it doesn't wait for a bid/pass click. Poll so the UI reflects bot bids
  // and phase changes that happen without any action here.
  const busyRef = useRef(false);
  useEffect(() => {
    busyRef.current = busy;
  }, [busy]);

  useEffect(() => {
    if (!sessionId) return undefined;
    const interval = setInterval(async () => {
      if (busyRef.current) return;
      try {
        const next = await api.getGame(sessionId);
        setState(next);
        if (next.phase === "game_over") {
          clearInterval(interval);
        }
      } catch {
        // Transient poll failure; the next tick will retry.
      }
    }, POLL_MS);
    return () => clearInterval(interval);
  }, [sessionId]);

  async function run(action) {
    setBusy(true);
    setError(null);
    try {
      const next = await action();
      setState(next);
      setSessionId(next.session_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const startGame = () => run(() => api.newGame());
  const doBid = (amount) => run(() => api.bid(sessionId, amount));
  const doPass = () => run(() => api.pass(sessionId));
  const doSkip = () => run(() => api.skip(sessionId));
  const doAdvance = () => run(() => api.advance(sessionId));
  const doTogglePause = () =>
    run(() => (state.paused ? api.resume(sessionId) : api.pause(sessionId)));
  const doCompleteSimulation = () => {
    if (!window.confirm("Fast-forward the rest of the auction to the end? You won't be able to bid on remaining players.")) {
      return;
    }
    run(() => api.completeSimulation(sessionId));
  };

  async function showRemainingPlayers() {
    setRemainingError(null);
    setRemainingPlayersOpen(true);
    setRemainingLoading(true);
    try {
      const data = await api.getRemainingPlayers(sessionId);
      setRemainingPlayers(data);
    } catch (err) {
      setRemainingError(err.message);
    } finally {
      setRemainingLoading(false);
    }
  }

  async function selectTeam(teamKey, knownSummary) {
    setTeamError(null);
    if (knownSummary && knownSummary.squad) {
      // Already have full detail (the user's own team ships with the main state).
      setSelectedTeam(knownSummary);
      return;
    }
    setSelectedTeam({ name: "", key: teamKey });
    setTeamLoading(true);
    try {
      const detail = await api.getTeam(sessionId, teamKey);
      setSelectedTeam(detail);
    } catch (err) {
      setTeamError(err.message);
    } finally {
      setTeamLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <div>
          <h1>Cricket Auction Simulator</h1>
          {state && (
            <p className="live-note">
              {state.paused
                ? "Auction paused - bid, pass, and skip still work."
                : "Live auction - bid or pass anytime, or just watch."}
            </p>
          )}
        </div>
        <div className="header-buttons">
          <button onClick={startGame} disabled={busy}>
            {state ? "Restart Game" : "Start New Game"}
          </button>
          {state && state.phase !== "game_over" && (
            <button onClick={doTogglePause} disabled={busy} className="pause-button">
              {state.paused ? "Resume Auction" : "Pause Auction"}
            </button>
          )}
          {state && state.phase !== "game_over" && (
            <button onClick={doCompleteSimulation} disabled={busy}>
              Complete Simulation
            </button>
          )}
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {state && (
        <div className="layout">
          <div className="column main-column">
            <PlayerCard player={state.current_player} />
            <AuctionStatus state={state} onShowRemainingPlayers={showRemainingPlayers} />
            <Controls
              state={state}
              onBid={doBid}
              onPass={doPass}
              onSkip={doSkip}
              onAdvance={doAdvance}
              busy={busy}
            />
          </div>
          <div className="column">
            <BidderSummary title="Your Team" summary={state.user} onSelectTeam={selectTeam} />
            <RivalsPanel rivals={state.rivals} onSelectTeam={selectTeam} />
          </div>
          <div className="column">
            <ActivityFeed events={state.event_log} />
          </div>
        </div>
      )}

      {selectedTeam && (
        <SquadModal
          team={selectedTeam.name ? selectedTeam : null}
          loading={teamLoading}
          error={teamError}
          onClose={() => setSelectedTeam(null)}
        />
      )}

      {remainingPlayersOpen && (
        <PlayerListModal
          data={remainingPlayers}
          loading={remainingLoading}
          error={remainingError}
          onClose={() => {
            setRemainingPlayersOpen(false);
            setRemainingPlayers(null);
          }}
        />
      )}
    </div>
  );
}
