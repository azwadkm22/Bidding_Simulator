import { useEffect, useMemo, useRef, useState } from "react";
import * as api from "./api";
import "./App.css";

const POLL_MS = 1000;

// Emoji flags per supported nationality (Player/player.py). West Indies has
// no country flag emoji, so it gets a maroon "WI" badge instead. Unknown
// nationalities render nothing rather than a wrong flag.
const NATIONALITY_FLAGS = {
  Bangladeshi: "\u{1F1E7}\u{1F1E9}",
  Australia: "\u{1F1E6}\u{1F1FA}",
  "South Africa": "\u{1F1FF}\u{1F1E6}",
  "New Zealand": "\u{1F1F3}\u{1F1FF}",
  England: "\u{1F3F4}\u{E0067}\u{E0062}\u{E0065}\u{E006E}\u{E0067}\u{E007F}",
};

function Flag({ nationality }) {
  if (nationality === "West Indies") {
    return (
      <span className="flag flag-badge" title={nationality}>
        WI
      </span>
    );
  }
  const flag = NATIONALITY_FLAGS[nationality];
  if (!flag) return null;
  return (
    <span className="flag" title={nationality === "Bangladeshi" ? "Bangladesh (Domestic)" : nationality}>
      {flag}
    </span>
  );
}

function PlayerCard({ player, onViewPlayer, onToggleShortlist }) {
  if (!player) return <div className="panel">No player on the block.</div>;
  return (
    <div className="panel">
      <h2>
        {player.shortlisted && "★ "}
        <Flag nationality={player.nationality} /> {player.name}{" "}
        <button className="link-button" onClick={() => onViewPlayer(player.player_id)}>
          [View Stats]
        </button>{" "}
        <button className="link-button" onClick={() => onToggleShortlist(player.player_id)}>
          [{player.shortlisted ? "Remove from" : "Add to"} Shortlist]
        </button>
      </h2>
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
          {state.last_result.type === "sold" && state.last_result.deal_grade && (
            <span className={`grade-badge grade-${state.last_result.deal_grade}`}>
              Grade {state.last_result.deal_grade}
            </span>
          )}
        </p>
      )}
    </div>
  );
}

function Controls({ state, onBid, onSkip, onAdvance, busy }) {
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

const BASE_PLAYER_COLUMNS = [
  { key: "name", label: "Name" },
  { key: "position", label: "Position" },
  { key: "player_type", label: "Type" },
  { key: "overall", label: "Overall" },
  { key: "batting", label: "Batting" },
  { key: "bowling", label: "Bowling" },
  { key: "fielding", label: "Fielding" },
];

// UI-only translations of the ratings-package role taxonomy (Player/ratings/
// generation.py's infer_role) - display labels only, never used for any
// internal lookup, filtering key, or game logic.
const ROLE_LABELS = {
  specialistBatter: { full: "Batsman", abbr: "BAT" },
  specialistBowler: { full: (isPace) => (isPace ? "Pacer" : "Spinner"), abbr: (isPace) => (isPace ? "PAC" : "SPN") },
  battingAllRounder: { full: "Allrounder Batsman", abbr: "ABT" },
  bowlingAllRounder: {
    full: (isPace) => (isPace ? "Allrounder Pacer" : "Allrounder Spinner"),
    abbr: (isPace) => (isPace ? "APC" : "ASP"),
  },
  balancedAllRounder: { full: "Allrounder", abbr: "ALL" },
  wicketkeeperBatter: { full: "Wicketkeeper", abbr: "WK" },
};

function roleLabel(role, isPace, form) {
  const entry = ROLE_LABELS[role];
  if (!entry) return role;
  const value = entry[form];
  return typeof value === "function" ? value(isPace) : value;
}

// "attackingTechnique" -> "Attacking Technique" - used wherever a raw camelCase
// attribute key would otherwise be shown to the user as-is.
function humanizeAttrName(attr) {
  const spaced = attr.replace(/([a-z])([A-Z])/g, "$1 $2");
  return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

const GRADE_RANK = { A: 4, B: 3, C: 2, D: 1 };

function sortableValue(player, key) {
  const v = player[key];
  if (key === "deal_grade") return GRADE_RANK[v] ?? 0;
  return v ?? 0;
}

// Shared by the squad viewer and the remaining-players list: a position
// filter plus click-to-sort columns. `extraColumns` are appended after the
// base stat columns (e.g. estimated value for the remaining-players list, or
// price paid + deal grade for a squad).
function PlayerTable({ players, extraColumns, emptyMessage, rowClassName, onViewPlayer, onToggleShortlist }) {
  const [positionFilter, setPositionFilter] = useState("All");
  const [typeFilter, setTypeFilter] = useState("All");
  const [sortKey, setSortKey] = useState(extraColumns[0].key);
  const [sortDir, setSortDir] = useState("desc");
  const [statKey, setStatKey] = useState("batting");
  const [statMin, setStatMin] = useState("");

  const columns = [...BASE_PLAYER_COLUMNS, ...extraColumns];
  // Only numeric columns make sense for a ">=" threshold filter - name/
  // position/grade/buyer are all strings, so exclude by actual value type
  // rather than hardcoding every string-valued column key.
  const statColumns = columns.filter(
    (c) =>
      c.key !== "name" &&
      c.key !== "position" &&
      c.key !== "player_type" &&
      c.key !== "deal_grade" &&
      !players.some((p) => typeof p[c.key] === "string"),
  );

  const positions = useMemo(
    () => ["All", ...new Set(players.map((p) => p.position))].sort(),
    [players],
  );

  const visiblePlayers = useMemo(() => {
    let filtered =
      positionFilter === "All" ? players : players.filter((p) => p.position === positionFilter);
    if (typeFilter !== "All") filtered = filtered.filter((p) => p.player_type === typeFilter);
    const threshold = statMin === "" ? null : Number(statMin);
    if (threshold !== null && !Number.isNaN(threshold)) {
      filtered = filtered.filter((p) => (p[statKey] ?? 0) >= threshold);
    }
    return [...filtered].sort((a, b) => {
      const va = sortableValue(a, sortKey);
      const vb = sortableValue(b, sortKey);
      const cmp = typeof va === "string" ? va.localeCompare(vb) : va - vb;
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [players, positionFilter, typeFilter, statKey, statMin, sortKey, sortDir]);

  function toggleSort(key) {
    if (key === sortKey) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir(key === "name" || key === "position" || key === "player_type" ? "asc" : "desc");
    }
  }

  return (
    <>
      <div className="player-filters">
        <select value={positionFilter} onChange={(e) => setPositionFilter(e.target.value)}>
          {positions.map((pos) => (
            <option key={pos} value={pos}>
              {pos}
            </option>
          ))}
        </select>
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} title="Filter by Domestic/International">
          <option value="All">All Types</option>
          <option value="Domestic">Domestic</option>
          <option value="International">International</option>
        </select>
        <select value={statKey} onChange={(e) => setStatKey(e.target.value)}>
          {statColumns.map((col) => (
            <option key={col.key} value={col.key}>
              {col.label}
            </option>
          ))}
        </select>
        <span>&ge;</span>
        <input
          type="number"
          placeholder="min"
          value={statMin}
          onChange={(e) => setStatMin(e.target.value)}
          className="stat-filter-input"
        />
        {statMin !== "" && (
          <button className="link-button" onClick={() => setStatMin("")}>
            Clear
          </button>
        )}
        <span className="filter-count">
          Showing {visiblePlayers.length} of {players.length}
        </span>
      </div>
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>
                <button className="sort-header" onClick={() => toggleSort(col.key)}>
                  {col.label}
                  {sortKey === col.key ? (sortDir === "asc" ? " ▲" : " ▼") : ""}
                </button>
              </th>
            ))}
            {onToggleShortlist && <th>Shortlist</th>}
          </tr>
        </thead>
        <tbody>
          {visiblePlayers.map((p) => (
            <tr key={p.player_id} className={rowClassName ? rowClassName(p) : undefined}>
              <td>
                {onViewPlayer ? (
                  <button className="link-button" onClick={() => onViewPlayer(p.player_id)}>
                    <Flag nationality={p.nationality} /> {p.name}
                  </button>
                ) : (
                  <>
                    <Flag nationality={p.nationality} /> {p.name}
                  </>
                )}{" "}
                ({roleLabel(p.role, p.bowling_type === "Pacer", "abbr")})
              </td>
              <td>{p.position}</td>
              <td>{p.player_type}</td>
              <td>{p.overall ?? "-"}</td>
              <td>{p.batting}</td>
              <td>{p.bowling}</td>
              <td>{p.fielding}</td>
              {extraColumns.map((col) => (
                <td key={col.key}>
                  {col.key === "deal_grade" ? (
                    p.deal_grade ? (
                      <span className={`grade-badge grade-${p.deal_grade}`}>{p.deal_grade}</span>
                    ) : (
                      "-"
                    )
                  ) : (
                    (p[col.key] ?? "-")
                  )}
                </td>
              ))}
              {onToggleShortlist && (
                <td>
                  <button
                    className={`shortlist-button${p.shortlisted ? " shortlist-button-active" : ""}`}
                    onClick={() => onToggleShortlist(p.player_id)}
                  >
                    {p.shortlisted ? "★ Shortlisted" : "☆ Add to Shortlist"}
                  </button>
                </td>
              )}
            </tr>
          ))}
          {visiblePlayers.length === 0 && (
            <tr>
              <td colSpan={onToggleShortlist ? columns.length + 1 : columns.length}>{emptyMessage}</td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
}

function SquadModal({ team, loading, error, onClose, onViewStartingEleven, onViewPlayer }) {
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
              {team.trait && ` · Bidder trait: ${team.trait}`}{" "}
              <button className="link-button" onClick={() => onViewStartingEleven(team.key)}>
                [View Starting XI]
              </button>
            </p>
            {team.composition && (
              <p>
                Batsmen: {team.composition.batsmen} · Bowlers: {team.composition.bowlers} ·
                Allrounders: {team.composition.allrounders} · Wicketkeepers:{" "}
                {team.composition.wicketkeepers}
              </p>
            )}
            <PlayerTable
              players={team.squad || []}
              extraColumns={[
                { key: "selling_price", label: "Price Paid" },
                { key: "deal_grade", label: "Grade" },
              ]}
              emptyMessage="No players bought yet."
              onViewPlayer={onViewPlayer}
            />
            {team.shortlist && (
              <details className="shortlist-details">
                <summary>Bidder Shortlist ({team.shortlist.length})</summary>
                <p className="live-note">
                  Players this bidder targeted before the auction started - fixed for the whole
                  game, so one already sold (to anyone) just shows a price paid below.
                </p>
                <PlayerTable
                  players={team.shortlist}
                  extraColumns={[
                    { key: "selling_price", label: "Price Paid" },
                    { key: "deal_grade", label: "Grade" },
                  ]}
                  emptyMessage="Nothing shortlisted."
                  onViewPlayer={onViewPlayer}
                />
              </details>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function PlayerListModal({ data, loading, error, onClose, onViewPlayer, onToggleShortlist }) {
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
          <PlayerTable
            players={data.players}
            extraColumns={[{ key: "estimated_price", label: "Est. Value" }]}
            emptyMessage="No players match this filter."
            onViewPlayer={onViewPlayer}
            onToggleShortlist={onToggleShortlist}
          />
        )}
      </div>
    </div>
  );
}

function StartingElevenModal({ data, loading, error, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{data ? `${data.name} - Starting XI` : "Starting XI"}</h2>
          <button onClick={onClose}>Close</button>
        </div>
        {loading && <p>Building lineup...</p>}
        {error && <p className="error-banner">{error}</p>}
        {data && !data.available && <p>{data.reason}</p>}
        {data && data.available && (
          <>
            <p>
              Batting: {data.batting_rating} · Bowling: {data.bowling_rating} · Fielding:{" "}
              {data.fielding_rating}
            </p>
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Position</th>
                  <th>Batting Order</th>
                  <th>Batting</th>
                  <th>Bowling</th>
                </tr>
              </thead>
              <tbody>
                {data.lineup.map((p, i) => (
                  <tr key={p.player_id}>
                    <td>{i + 1}</td>
                    <td>
                      <Flag nationality={p.nationality} /> {p.name} ({roleLabel(p.role, p.bowling_type === "Pacer", "abbr")})
                    </td>
                    <td>{p.position}</td>
                    <td>{p.batting_order}</td>
                    <td>{p.batting}</td>
                    <td>{p.bowling}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <h3>Bench</h3>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Position</th>
                  <th>Batting</th>
                  <th>Bowling</th>
                </tr>
              </thead>
              <tbody>
                {data.bench.map((p) => (
                  <tr key={p.player_id}>
                    <td>
                      <Flag nationality={p.nationality} /> {p.name} ({roleLabel(p.role, p.bowling_type === "Pacer", "abbr")})
                    </td>
                    <td>{p.position}</td>
                    <td>{p.batting}</td>
                    <td>{p.bowling}</td>
                  </tr>
                ))}
                {data.bench.length === 0 && (
                  <tr>
                    <td colSpan="4">No bench players.</td>
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

function GameSummary({ data, loading, error, onViewPlayer }) {
  if (loading) return <div className="panel">Building summary...</div>;
  if (error) return <div className="panel error-banner">{error}</div>;
  if (!data) return null;

  return (
    <div className="game-summary">
      <h2>Auction Complete</h2>

      <section className="panel">
        <h3>Sold Players ({data.sold_players.length})</h3>
        <p className="filter-count">{data.unsold_count} player(s) went unsold.</p>
        <PlayerTable
          players={data.sold_players}
          extraColumns={[
            { key: "selling_price", label: "Price Paid" },
            { key: "buyer", label: "Buyer" },
            { key: "deal_grade", label: "Grade" },
          ]}
          emptyMessage="No players were sold."
          rowClassName={(p) => (p.is_user ? "your-purchase" : undefined)}
          onViewPlayer={onViewPlayer}
        />
      </section>

      <section className="panel">
        <h3>Team Starting XIs</h3>
        <table>
          <thead>
            <tr>
              <th>Team</th>
              <th>Squad</th>
              <th>Budget Left</th>
              <th>Batting</th>
              <th>Bowling</th>
              <th>Fielding</th>
            </tr>
          </thead>
          <tbody>
            {data.teams.map((t) => (
              <tr key={t.key} className={t.is_user ? "your-purchase" : undefined}>
                <td>
                  {t.name}
                  {t.is_user ? " (You)" : ""}
                </td>
                <td>{t.squad_size}</td>
                <td>{t.budget}</td>
                {t.starting_eleven.available ? (
                  <>
                    <td>{t.starting_eleven.batting_rating}</td>
                    <td>{t.starting_eleven.bowling_rating}</td>
                    <td>{t.starting_eleven.fielding_rating}</td>
                  </>
                ) : (
                  <td colSpan="3" title={t.starting_eleven.reason}>
                    Not available - {t.starting_eleven.reason}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </section>
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

const ALL_PLAYERS_KEY = "all_players";

const POOL_CATEGORIES = [
  { key: ALL_PLAYERS_KEY, label: "All Players" },
  { key: "most_expensive", label: "Most Expensive" },
  { key: "top_batsmen", label: "Top Batsmen" },
  { key: "top_bowlers", label: "Top Bowlers" },
  { key: "top_allrounders", label: "Top Allrounders" },
  { key: "top_wicketkeepers", label: "Top Wicketkeepers" },
  { key: "top_openers", label: "Top Openers" },
  { key: "top_pacers", label: "Top Pacers" },
  { key: "top_spinners", label: "Top Spinners" },
];

function PoolCategoryPicker({ pool, onViewPlayer, onToggleShortlist }) {
  const [category, setCategory] = useState(ALL_PLAYERS_KEY);
  const [allPlayers, setAllPlayers] = useState(null);
  const [allPlayersLoading, setAllPlayersLoading] = useState(false);
  const [allPlayersError, setAllPlayersError] = useState(null);

  useEffect(() => {
    if (category !== ALL_PLAYERS_KEY) return;
    setAllPlayersError(null);
    setAllPlayersLoading(true);
    api
      .getPoolPlayers(pool.pool_id)
      .then((data) => setAllPlayers(data.players))
      .catch((err) => setAllPlayersError(err.message))
      .finally(() => setAllPlayersLoading(false));
    // pool.count (not just pool.pool_id) is a dependency so a custom player
    // added via Create Player - which bumps count without changing pool_id -
    // invalidates this cache instead of leaving it stale until a full reload.
  }, [category, pool.pool_id, pool.count]);

  const players = category === ALL_PLAYERS_KEY ? allPlayers || [] : pool[category];

  // Toggling refreshes the parent's `pool` (so category lists like
  // top_batsmen pick up the change), but the "All Players" list is fetched
  // and cached separately here - flip it locally too instead of a second
  // round trip, so the star updates immediately either way.
  async function handleToggleShortlist(playerId) {
    await onToggleShortlist(playerId);
    setAllPlayers((prev) =>
      prev ? prev.map((p) => (p.player_id === playerId ? { ...p, shortlisted: !p.shortlisted } : p)) : prev,
    );
  }

  return (
    <div className="panel">
      <div className="pool-category-header">
        <h4>Player Categories</h4>
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {POOL_CATEGORIES.map((c) => (
            <option key={c.key} value={c.key}>
              {c.label}
            </option>
          ))}
        </select>
      </div>
      {category === ALL_PLAYERS_KEY && allPlayersLoading && <p>Loading all players...</p>}
      {category === ALL_PLAYERS_KEY && allPlayersError && (
        <p className="error-banner">{allPlayersError}</p>
      )}
      {!(category === ALL_PLAYERS_KEY && allPlayersLoading) && (
        <PlayerTable
          players={players}
          extraColumns={[{ key: "estimated_price", label: "Est. Value" }]}
          emptyMessage="None."
          onViewPlayer={onViewPlayer}
          onToggleShortlist={handleToggleShortlist}
        />
      )}
    </div>
  );
}

function PoolScreen({
  pool,
  loading,
  error,
  genSeed,
  setGenSeed,
  genCount,
  setGenCount,
  genInternational,
  setGenInternational,
  onGenerate,
  onStartAuction,
  onViewPlayer,
  onOpenCreatePlayer,
  onToggleShortlist,
  busy,
}) {
  return (
    <div className="pool-screen">
      <div className="panel">
        <h2>Generate Players</h2>
        <p className="live-note">
          Generate a player pool first, review it, then start an auction using it - the same
          pool can be reused for more than one auction.
        </p>
        <div className="pool-form">
          <input
            type="number"
            placeholder="Seed (optional)"
            value={genSeed}
            onChange={(e) => setGenSeed(e.target.value)}
            className="seed-input"
            title="Same seed reproduces the same player pool"
          />
          <input
            type="number"
            placeholder="Count (default 250)"
            value={genCount}
            onChange={(e) => setGenCount(e.target.value)}
            className="seed-input"
          />
          <input
            type="number"
            min="0"
            placeholder="International players (default 0)"
            value={genInternational}
            onChange={(e) => setGenInternational(e.target.value)}
            className="seed-input"
            title="How many of the generated players are International; the rest are Domestic"
          />
          <button onClick={onGenerate} disabled={loading}>
            {pool ? "Generate Different Pool" : "Generate Players"}
          </button>
          <button onClick={onOpenCreatePlayer}>Create Player</button>
        </div>
        {error && <p className="error-banner">{error}</p>}
      </div>

      {loading && <div className="panel">Generating players...</div>}

      {pool && !loading && (
        <>
          <div className="panel">
            <h3>Pool Summary</h3>
            <p>
              Seed: {pool.seed} · {pool.count} players
            </p>
            <p>
              {Object.entries(pool.position_counts)
                .map(([pos, n]) => `${pos}: ${n}`)
                .join(" · ")}
            </p>
            <p>
              Domestic: {pool.player_type_counts?.Domestic || 0} · International:{" "}
              {pool.player_type_counts?.International || 0}
            </p>
            <p>
              Pacers: {pool.bowling_type_counts.Pacer || 0} · Spinners:{" "}
              {pool.bowling_type_counts.Spinner || 0}
            </p>
            <p>
              Rated 80+: {pool.players_above_80} · Rated 90+: {pool.players_above_90}
            </p>
            <button onClick={onStartAuction} disabled={busy}>
              Start Auction with this Pool
            </button>
          </div>

          <PoolCategoryPicker pool={pool} onViewPlayer={onViewPlayer} onToggleShortlist={onToggleShortlist} />
        </>
      )}
    </div>
  );
}

const CUSTOM_PLAYER_ROLES = [
  "specialistBatter", "specialistBowler", "battingAllRounder",
  "bowlingAllRounder", "balancedAllRounder", "wicketkeeperBatter",
];

const CUSTOM_PLAYER_CATEGORY_TITLES = {
  batting: "Batting",
  paceBowling: "Pace Bowling",
  spinBowling: "Spin Bowling",
  fielding: "Fielding",
  wicketkeeping: "Wicketkeeping",
  physical: "Physical",
  mentality: "Mentality",
};

// Maps a calculate_player_ratings() key onto the skill label SKILL_ATTRIBUTE_PATHS
// (below) understands, so hovering a rating badge here can reuse the exact same
// highlight lookup as the read-only Player Detail view.
const RATING_KEY_TO_SKILL_LABEL = {
  batting: "Batting",
  paceBowling: "Bowling",
  spinBowling: "Bowling",
  fielding: "Fielding",
  wicketkeeping: "Keeping",
  mentality: "Mentality",
  physical: "Physical",
};

// Every editable attribute is derived from the weight tables themselves
// (plus vsSpin/vsPace, which aren't in a weight table - see BATTING_VS_BLEND)
// rather than hardcoded here, so the form never drifts out of sync with
// Player/ratings/weights.py.
function buildCustomPlayerAttributeGroups(weightTables) {
  const groups = {};
  for (const table of Object.values(weightTables.tables)) {
    for (const [path] of table) {
      if (path.startsWith("DERIVED.")) continue;
      const [category, attr] = path.split(".");
      if (!groups[category]) groups[category] = new Set();
      groups[category].add(attr);
    }
  }
  groups.batting = groups.batting || new Set();
  groups.batting.add("vsSpin");
  groups.batting.add("vsPace");
  return groups;
}

function initialCustomPlayerValues(groups) {
  const values = {};
  for (const [category, attrs] of Object.entries(groups)) {
    values[category] = {};
    for (const attr of attrs) {
      values[category][attr] = attr === "vsSpin" || attr === "vsPace" ? 5 : 50;
    }
  }
  return values;
}

function CreatePlayerScreen({ poolId, onClose, onPlayerAdded }) {
  const [weightTables, setWeightTables] = useState(null);
  const [loadError, setLoadError] = useState(null);
  const [groups, setGroups] = useState(null);
  const [values, setValues] = useState(null);
  const [form, setForm] = useState({
    name: "Custom Player",
    position: "Batsmen",
    role: "specialistBatter",
    batting_hand: "Right",
    bowling_type: "Pacer",
    batting_order: "Middle Order",
    fame: 50,
    player_type: "Domestic",
  });
  // Mirrors infer_role() (Player/ratings/generation.py) exactly: a role's
  // bowling style is never an independent choice in the real generator -
  // it's "none" for the two non-bowling roles, otherwise whatever bowling_type
  // says. Deriving it here (instead of a separate dropdown) is what fixed
  // Overall silently only ever using the specialistBatter weights - a
  // forgotten "none" selection was starving every bowling-inclusive role of
  // its bowling rating, which calculate_overall_rating then reported as
  // missing rather than computing.
  const primaryBowlingStyle =
    form.role === "specialistBatter" || form.role === "wicketkeeperBatter"
      ? "none"
      : form.bowling_type === "Pacer"
        ? "pace"
        : "spin";
  const [preview, setPreview] = useState(null);
  const [previewError, setPreviewError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);
  const [saveError, setSaveError] = useState(null);
  const [showBreakdown, setShowBreakdown] = useState(false);
  const [hoveredSkill, setHoveredSkill] = useState(null);

  useEffect(() => {
    api
      .getWeightTables()
      .then((data) => {
        setWeightTables(data);
        const g = buildCustomPlayerAttributeGroups(data);
        setGroups(g);
        setValues(initialCustomPlayerValues(g));
      })
      .catch((err) => setLoadError(err.message));
  }, []);

  useEffect(() => {
    if (!values) return undefined;
    const timeout = setTimeout(() => {
      api
        .previewCustomPlayer({
          role: form.role,
          primary_bowling_style: primaryBowlingStyle,
          attributes: values,
        })
        .then((data) => {
          setPreview(data);
          setPreviewError(null);
        })
        .catch((err) => setPreviewError(err.message));
    }, 250);
    return () => clearTimeout(timeout);
  }, [values, form.role, primaryBowlingStyle]);

  function updateForm(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function updateValue(category, attr, raw) {
    const isVsAttr = category === "batting" && (attr === "vsSpin" || attr === "vsPace");
    const [min, max] = isVsAttr ? [1, 10] : [0, 99];
    const num = Number(raw);
    const clamped = Number.isNaN(num) ? min : Math.min(max, Math.max(min, num));
    setValues((prev) => ({
      ...prev,
      [category]: { ...prev[category], [attr]: clamped },
    }));
  }

  function weightFor(category, attr) {
    if (!weightTables) return null;
    const tableName =
      category === "physical" ? "physicalSummary" : category === "mentality" ? "mentalitySummary" : category;
    const table = weightTables.tables[tableName] || [];
    const entry = table.find(([path]) => path === `${category}.${attr}`);
    return entry ? entry[1] : null;
  }

  async function handleSave() {
    setSaving(true);
    setSaveError(null);
    setSaveMessage(null);
    try {
      const created = await api.createCustomPlayer(poolId, {
        role: form.role,
        primary_bowling_style: primaryBowlingStyle,
        name: form.name,
        position: form.position,
        batting_hand: form.batting_hand,
        bowling_type: form.bowling_type,
        batting_order: form.batting_order,
        fame: Number(form.fame),
        player_type: form.player_type,
        attributes: values,
      });
      setSaveMessage(
        `Added "${created.name}" to the pool - Batting ${created.core.batting}, Bowling ${created.core.bowling}, Fielding ${created.core.fielding}.`,
      );
      if (onPlayerAdded) onPlayerAdded();
    } catch (err) {
      setSaveError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loadError) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <p className="error-banner">{loadError}</p>
        </div>
      </div>
    );
  }

  if (!weightTables || !groups || !values) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal" onClick={(e) => e.stopPropagation()}>
          <p>Loading attribute definitions...</p>
        </div>
      </div>
    );
  }

  const bowlingCategory = form.bowling_type === "Pacer" ? "paceBowling" : "spinBowling";
  const categoryOrder = ["batting", bowlingCategory, "fielding", "wicketkeeping", "physical", "mentality"];
  const hasPace = form.bowling_type === "Pacer";
  const highlightPaths = hoveredSkill ? new Set(skillPathsFor(hoveredSkill, hasPace)) : null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal create-player-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create Player</h2>
          <button onClick={onClose}>Close</button>
        </div>
        <p className="live-note">
          Set detailed attributes below and watch the computed Core Skills update live - a
          sandbox for tuning weightage, not a randomly generated player.
        </p>

        <div className="create-player-basics">
          <input value={form.name} onChange={(e) => updateForm("name", e.target.value)} placeholder="Name" />
          <select value={form.position} onChange={(e) => updateForm("position", e.target.value)}>
            {["Batsmen", "Bowler", "Allrounder", "Wicketkeeper", "Trainee"].map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <select value={form.role} onChange={(e) => updateForm("role", e.target.value)}>
            {CUSTOM_PLAYER_ROLES.map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
          <select value={form.bowling_type} onChange={(e) => updateForm("bowling_type", e.target.value)}>
            <option value="Pacer">Pacer</option>
            <option value="Spinner">Spinner</option>
          </select>
          <span className="live-note" title="Derived from Role + Bowling Type, same as the real generator - not independently settable">
            {primaryBowlingStyle === "none" ? "Doesn't bowl" : `Bowls ${primaryBowlingStyle}`}
          </span>
          <select value={form.player_type} onChange={(e) => updateForm("player_type", e.target.value)}>
            <option value="Domestic">Domestic</option>
            <option value="International">International</option>
          </select>
          <select value={form.batting_hand} onChange={(e) => updateForm("batting_hand", e.target.value)}>
            <option value="Right">Right-Handed</option>
            <option value="Left">Left-Handed</option>
          </select>
          <select value={form.batting_order} onChange={(e) => updateForm("batting_order", e.target.value)}>
            {["Opener", "Top Order", "Middle Order", "Low Order"].map((o) => (
              <option key={o} value={o}>{o}</option>
            ))}
          </select>
        </div>

        <div className="rating-badges">
          {preview &&
            Object.entries(preview.ratings).map(([key, rating]) => {
              const skillLabel = RATING_KEY_TO_SKILL_LABEL[key];
              return (
                <RatingBadge
                  key={key}
                  label={key}
                  rating={rating}
                  hoverable={Boolean(skillLabel)}
                  onHover={() => setHoveredSkill(skillLabel)}
                  onUnhover={() => setHoveredSkill(null)}
                />
              );
            })}
          {preview && (
            <button className="link-button breakdown-toggle" onClick={() => setShowBreakdown((v) => !v)}>
              {showBreakdown ? "Hide Breakdown" : "Show Breakdown"}
            </button>
          )}
        </div>
        {previewError && <p className="error-banner">{previewError}</p>}

        {preview && showBreakdown && (
          <div className="create-player-breakdowns">
            {Object.entries(preview.ratings)
              .filter(([, rating]) => rating.breakdown)
              .map(([key, rating]) => (
                <details key={key} className="breakdown-details">
                  <summary>
                    {key} breakdown ({rating.displayed ?? "-"})
                  </summary>
                  <table className="breakdown-table">
                    <thead>
                      <tr>
                        <th>Path</th>
                        <th>Value</th>
                        <th>Weight %</th>
                        <th>Contribution</th>
                      </tr>
                    </thead>
                    <tbody>
                      {rating.breakdown.map((entry) => (
                        <tr key={entry.path}>
                          <td>{entry.path}</td>
                          <td>{entry.value}</td>
                          <td>{entry.weight}</td>
                          <td>{entry.contribution}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </details>
              ))}
          </div>
        )}

        <div className="create-player-attribute-groups">
          {categoryOrder
            .filter((category) => groups[category])
            .map((category) => (
              <div key={category} className="attribute-section">
                <h4>{CUSTOM_PLAYER_CATEGORY_TITLES[category] || category}</h4>
                <div className="attribute-grid">
                  {Array.from(groups[category])
                    .sort()
                    .map((attr) => {
                      const weight = weightFor(category, attr);
                      const isVsAttr = category === "batting" && (attr === "vsSpin" || attr === "vsPace");
                      const highlighted = highlightPaths && highlightPaths.has(`${category}.${attr}`);
                      return (
                        <div
                          key={attr}
                          className={`attribute-cell attribute-cell-editable${highlighted ? " attribute-cell-highlighted" : ""}`}
                        >
                          <span className="attribute-label">
                            {humanizeAttrName(attr)}
                            {weight != null && <span className="attribute-weight-badge">{weight}%</span>}
                          </span>
                          <input
                            type="number"
                            min={isVsAttr ? 1 : 0}
                            max={isVsAttr ? 10 : 99}
                            value={values[category][attr]}
                            onChange={(e) => updateValue(category, attr, e.target.value)}
                            className="attribute-value-input"
                          />
                        </div>
                      );
                    })}
                </div>
              </div>
            ))}
        </div>

        <div className="create-player-actions">
          {poolId ? (
            <button onClick={handleSave} disabled={saving}>
              {saving ? "Adding..." : "Add to Pool"}
            </button>
          ) : (
            <p className="live-note">Generate a pool first to add this player to it.</p>
          )}
          {saveMessage && <p className="live-note">{saveMessage}</p>}
          {saveError && <p className="error-banner">{saveError}</p>}
        </div>
      </div>
    </div>
  );
}

// Mirrors the attribute paths (not the weight percentages) in
// Player/ratings/weights.py, so hovering a core-skill badge can highlight
// exactly the attributes that feed it. DERIVED.*VariationQuality entries are
// left out here since they come from the whole repertoire section, not a
// single attribute - see repertoireStyleForSkill below.
const SKILL_ATTRIBUTE_PATHS = {
  Batting: [
    "batting.timing", "batting.shotSelection", "physical.footwork",
    "batting.defensiveTechnique", "batting.attackingTechnique", "batting.placement",
    "physical.strength", "batting.offside", "batting.legside", "batting.straight",
    "mentality.composure", "mentality.concentration", "mentality.decisionMaking", "mentality.discipline",
    "physical.runningSpeed", "physical.agility", "physical.stamina", "physical.balance",
  ],
  paceBowling: [
    "paceBowling.pace", "paceBowling.lineControl", "paceBowling.lengthControl",
    "paceBowling.releaseConsistency", "paceBowling.swing", "paceBowling.seam",
    "paceBowling.bounce", "paceBowling.yorker", "paceBowling.bouncer",
    "paceBowling.disguise", "mentality.tacticalAwareness", "mentality.composure",
    "physical.stamina",
  ],
  spinBowling: [
    "spinBowling.turn", "spinBowling.lineControl", "spinBowling.lengthControl",
    "spinBowling.releaseConsistency", "spinBowling.drift", "spinBowling.dip",
    "spinBowling.flightControl", "spinBowling.paceVariation", "spinBowling.disguise",
    "mentality.tacticalAwareness", "mentality.composure", "physical.stamina",
  ],
  Fielding: [
    "fielding.catching", "fielding.groundFielding", "fielding.positioning",
    "mentality.anticipation", "physical.reflexes", "fielding.throwAccuracy",
    "fielding.throwPower", "fielding.pickupAndRelease", "physical.runningSpeed",
    "physical.agility", "fielding.diving", "fielding.boundaryAwareness", "physical.balance",
  ],
  Keeping: [
    "wicketkeeping.glovework", "physical.footwork", "physical.reflexes",
    "mentality.anticipation", "wicketkeeping.standingUp", "wicketkeeping.standingBack",
    "wicketkeeping.stumping", "wicketkeeping.legSideCollection", "fielding.diving",
    "wicketkeeping.byesPrevention", "fielding.catching", "mentality.concentration",
    "mentality.decisionMaking", "physical.balance",
  ],
  Mentality: [
    "mentality.concentration", "mentality.composure", "mentality.decisionMaking",
    "mentality.tacticalAwareness", "mentality.adaptability", "mentality.discipline",
    "mentality.resilience", "mentality.gameReading",
  ],
  Physical: [
    "physical.strength", "physical.stamina", "physical.runningSpeed", "physical.agility",
    "physical.reflexes", "physical.footwork", "physical.balance", "physical.recovery",
  ],
};

function skillPathsFor(label, hasPace) {
  if (label === "Bowling") return SKILL_ATTRIBUTE_PATHS[hasPace ? "paceBowling" : "spinBowling"];
  return SKILL_ATTRIBUTE_PATHS[label] || [];
}

function repertoireStyleForSkill(label, hasPace) {
  return label === "Bowling" ? (hasPace ? "pace" : "spin") : null;
}

// vsPace/vsSpin are a 1-10 matchup rating (see Player/ratings/generation.py),
// not a 0-99 attribute, so they render as a filled/unfilled bar instead of a
// plain number - a different metric deserves a visually different cell.
const VS_MATCHUP_LABELS = { vsPace: "Against Pace", vsSpin: "Against Spin" };

function vsMatchupBar(rating) {
  const filled = Math.max(0, Math.min(10, Math.round(rating)));
  return "▰".repeat(filled) + "▱".repeat(10 - filled);
}

function AttributeGrid({ title, category, attributes, highlightPaths, highlightAll }) {
  const entries = Object.entries(attributes || {});
  if (entries.length === 0) return null;
  return (
    <div className="attribute-section">
      <h4>{title}</h4>
      <div className="attribute-grid">
        {entries.map(([key, value]) => {
          const path = `${category}.${key}`;
          const highlighted = highlightAll || (highlightPaths && highlightPaths.has(path));
          const vsLabel = category === "batting" ? VS_MATCHUP_LABELS[key] : null;
          return (
            <div key={key} className={`attribute-cell${highlighted ? " attribute-cell-highlighted" : ""}`}>
              <span className="attribute-label">{vsLabel || key}</span>
              <span className="attribute-value">{vsLabel ? vsMatchupBar(value) : Math.round(value)}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function RatingBadge({ label, rating, hoverable, onHover, onUnhover }) {
  if (!rating) return null;
  return (
    <div
      className={`rating-badge${hoverable ? " rating-badge-hoverable" : ""}`}
      onMouseEnter={hoverable ? onHover : undefined}
      onMouseLeave={hoverable ? onUnhover : undefined}
    >
      <span className="rating-badge-label">{label}</span>
      <span className="rating-badge-value">{rating.unavailable ? "-" : rating.displayed}</span>
    </div>
  );
}

function PlayerDetailModal({ data, loading, error, onClose }) {
  const [hoveredSkill, setHoveredSkill] = useState(null);
  const hasPace = Boolean(data && data.attributes.paceBowling && Object.keys(data.attributes.paceBowling).length > 0);
  const highlightPaths = hoveredSkill ? new Set(skillPathsFor(hoveredSkill, hasPace)) : null;
  const highlightRepertoireStyle = hoveredSkill ? repertoireStyleForSkill(hoveredSkill, hasPace) : null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{data ? <><Flag nationality={data.nationality} /> {data.name}</> : "Loading..."}</h2>
          <button onClick={onClose}>Close</button>
        </div>
        {loading && <p>Loading player...</p>}
        {error && <p className="error-banner">{error}</p>}
        {data && (
          <>
            <p>
              {roleLabel(data.role, data.primary_bowling_style === "pace", "full")}
              {" · "}{data.batting_hand}-Handed · {data.batting_order} · {data.player_type} ({data.nationality})
            </p>
            <div className="rating-badges">
              <RatingBadge label="Overall" rating={data.ratings.overall} />
              <RatingBadge
                label="Batting"
                rating={data.ratings.batting}
                hoverable
                onHover={() => setHoveredSkill("Batting")}
                onUnhover={() => setHoveredSkill(null)}
              />
              <RatingBadge
                label="Bowling"
                rating={data.ratings.paceBowling || data.ratings.spinBowling}
                hoverable
                onHover={() => setHoveredSkill("Bowling")}
                onUnhover={() => setHoveredSkill(null)}
              />
              <RatingBadge
                label="Fielding"
                rating={data.ratings.fielding}
                hoverable
                onHover={() => setHoveredSkill("Fielding")}
                onUnhover={() => setHoveredSkill(null)}
              />
              <RatingBadge
                label="Keeping"
                rating={data.ratings.wicketkeeping}
                hoverable
                onHover={() => setHoveredSkill("Keeping")}
                onUnhover={() => setHoveredSkill(null)}
              />
              <RatingBadge
                label="Mentality"
                rating={data.ratings.mentality}
                hoverable
                onHover={() => setHoveredSkill("Mentality")}
                onUnhover={() => setHoveredSkill(null)}
              />
              <RatingBadge
                label="Physical"
                rating={data.ratings.physical}
                hoverable
                onHover={() => setHoveredSkill("Physical")}
                onUnhover={() => setHoveredSkill(null)}
              />
            </div>

            <AttributeGrid title="Batting" category="batting" attributes={data.attributes.batting} highlightPaths={highlightPaths} />
            <AttributeGrid title="Pace Bowling" category="paceBowling" attributes={data.attributes.paceBowling} highlightPaths={highlightPaths} />
            <AttributeGrid title="Spin Bowling" category="spinBowling" attributes={data.attributes.spinBowling} highlightPaths={highlightPaths} />
            <AttributeGrid title="Fielding" category="fielding" attributes={data.attributes.fielding} highlightPaths={highlightPaths} />
            <AttributeGrid title="Wicketkeeping" category="wicketkeeping" attributes={data.attributes.wicketkeeping} highlightPaths={highlightPaths} />
            <AttributeGrid title="Physical" category="physical" attributes={data.attributes.physical} highlightPaths={highlightPaths} />
            <AttributeGrid title="Mentality" category="mentality" attributes={data.attributes.mentality} highlightPaths={highlightPaths} />
            {Object.entries(data.attributes.repertoire || {}).map(
              ([style, deliveries]) =>
                Object.keys(deliveries).length > 0 && (
                  <AttributeGrid
                    key={style}
                    title={`${style === "pace" ? "Pace" : "Spin"} Repertoire`}
                    category={`repertoire.${style}`}
                    attributes={deliveries}
                    highlightAll={highlightRepertoireStyle === style}
                  />
                ),
            )}
            <AttributeGrid title="Traits" category="traits" attributes={data.attributes.traits} highlightPaths={highlightPaths} />
            <AttributeGrid title="State" category="state" attributes={data.attributes.state} highlightPaths={highlightPaths} />
          </>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [state, setState] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [pool, setPool] = useState(null);
  const [poolLoading, setPoolLoading] = useState(false);
  const [poolError, setPoolError] = useState(null);
  const [genSeed, setGenSeed] = useState("");
  const [genCount, setGenCount] = useState("");
  const [genInternational, setGenInternational] = useState("");
  const [playerDetail, setPlayerDetail] = useState(null);
  const [playerDetailOpen, setPlayerDetailOpen] = useState(false);
  const [playerDetailLoading, setPlayerDetailLoading] = useState(false);
  const [playerDetailError, setPlayerDetailError] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teamLoading, setTeamLoading] = useState(false);
  const [teamError, setTeamError] = useState(null);
  const [remainingPlayers, setRemainingPlayers] = useState(null);
  const [remainingPlayersOpen, setRemainingPlayersOpen] = useState(false);
  const [remainingLoading, setRemainingLoading] = useState(false);
  const [remainingError, setRemainingError] = useState(null);
  const [startingEleven, setStartingEleven] = useState(null);
  const [startingElevenOpen, setStartingElevenOpen] = useState(false);
  const [startingElevenLoading, setStartingElevenLoading] = useState(false);
  const [startingElevenError, setStartingElevenError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState(null);
  const [view, setView] = useState("auction"); // "auction" | "summary"
  const [createPlayerOpen, setCreatePlayerOpen] = useState(false);
  const [stopOnShortlisted, setStopOnShortlisted] = useState(false);

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

  async function showSummary() {
    setSummaryError(null);
    setSummaryLoading(true);
    setView("summary");
    try {
      const data = await api.getSummary(sessionId);
      setSummary(data);
    } catch (err) {
      setSummaryError(err.message);
    } finally {
      setSummaryLoading(false);
    }
  }

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

  async function generatePool() {
    setPoolError(null);
    setPoolLoading(true);
    try {
      const data = await api.generatePool({ seed: genSeed, count: genCount, internationalCount: genInternational });
      setPool(data);
      setState(null);
      setSessionId(null);
    } catch (err) {
      setPoolError(err.message);
    } finally {
      setPoolLoading(false);
    }
  }

  async function refreshPoolAfterCustomPlayer() {
    if (!pool) return;
    try {
      const data = await api.getPoolSummary(pool.pool_id);
      setPool(data);
    } catch {
      // Non-fatal: the created player is already saved server-side even if
      // this refresh fails, so just leave the summary stale rather than
      // surfacing an error for a purely cosmetic refresh.
    }
  }

  async function doTogglePoolShortlist(playerId) {
    try {
      const data = await api.togglePoolShortlist(pool.pool_id, playerId);
      setPool(data);
    } catch (err) {
      setPoolError(err.message);
    }
  }

  async function showPlayerDetail(playerId) {
    // In an active game, use that game's own pool (mid-auction viewing);
    // otherwise fall back to whatever pool is loaded on the generation screen.
    const poolId = state ? state.pool_id : pool?.pool_id;
    if (!poolId) {
      setPlayerDetailOpen(true);
      setPlayerDetailError("This game wasn't started from a generated pool, so detailed stats aren't available.");
      return;
    }
    setPlayerDetailError(null);
    setPlayerDetailOpen(true);
    setPlayerDetailLoading(true);
    try {
      const data = await api.getPlayerDetail(poolId, playerId);
      setPlayerDetail(data);
    } catch (err) {
      setPlayerDetailError(err.message);
    } finally {
      setPlayerDetailLoading(false);
    }
  }

  const startAuctionFromPool = () => {
    setView("auction");
    setSummary(null);
    run(() => api.newGame(pool.pool_id));
  };

  const newPlayerPool = () => {
    setPool(null);
    setState(null);
    setSessionId(null);
    setView("auction");
    setSummary(null);
  };

  const doBid = (amount) => run(() => api.bid(sessionId, amount));
  const doSkip = () => run(() => api.skip(sessionId));
  const doAdvance = () => run(() => api.advance(sessionId));
  const doTogglePause = () =>
    run(() => (state.paused ? api.resume(sessionId) : api.pause(sessionId)));
  const doCompleteSimulation = () => {
    if (!window.confirm("Fast-forward the rest of the auction to the end? You won't be able to bid on remaining players.")) {
      return;
    }
    run(() => api.completeSimulation(sessionId, stopOnShortlisted));
  };
  const doCompleteRound = () => {
    if (
      !window.confirm(
        `Fast-forward the rest of Round ${state.round_number} (unsold players still come back up next round)?`,
      )
    ) {
      return;
    }
    run(() => api.completeRound(sessionId, stopOnShortlisted));
  };
  const doSkipPlayers = () => run(() => api.skipPlayers(sessionId, 10, stopOnShortlisted));
  const doToggleShortlist = async (playerId) => {
    await run(() => api.toggleShortlist(sessionId, playerId));
    // The Remaining Players modal fetches its own list separately from the
    // main game state, so a toggle made from there needs an explicit
    // refresh - otherwise its star/checkbox would stay stale until reopened.
    if (remainingPlayersOpen) {
      const data = await api.getRemainingPlayers(sessionId);
      setRemainingPlayers(data);
    }
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

  async function showStartingEleven(teamKey) {
    setStartingElevenError(null);
    setStartingElevenOpen(true);
    setStartingElevenLoading(true);
    try {
      const data = await api.getStartingEleven(sessionId, teamKey);
      setStartingEleven(data);
    } catch (err) {
      setStartingElevenError(err.message);
    } finally {
      setStartingElevenLoading(false);
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
              {state.phase === "game_over"
                ? "Auction complete."
                : state.paused
                  ? "Auction paused - bid, pass, and skip still work."
                  : "Live auction - bid or pass anytime, or just watch."}
            </p>
          )}
          {state && <p className="seed-note">Pool seed: {state.seed}</p>}
        </div>
        <div className="header-buttons">
          {pool && (
            <button onClick={startAuctionFromPool} disabled={busy}>
              {state ? "Restart Game" : "Start Auction"}
            </button>
          )}
          {(pool || state) && (
            <button onClick={newPlayerPool} disabled={busy}>
              New Player Pool
            </button>
          )}
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
          {state && state.phase !== "game_over" && (
            <button onClick={doCompleteRound} disabled={busy}>
              Complete Round {state.round_number}
            </button>
          )}
          {state && state.phase !== "game_over" && (
            <button onClick={doSkipPlayers} disabled={busy}>
              Skip Next 10 Players
            </button>
          )}
          {state && state.phase !== "game_over" && (
            <label className="stop-on-shortlisted-toggle" title="Applies to Complete Simulation, Complete Round, and Skip Next 10 Players">
              <input
                type="checkbox"
                checked={stopOnShortlisted}
                onChange={(e) => setStopOnShortlisted(e.target.checked)}
              />
              Stop at Shortlisted Player
            </label>
          )}
          {state && (
            <button onClick={view === "auction" ? showSummary : () => setView("auction")}>
              {view === "auction" ? "View Summary" : "Back to Auction"}
            </button>
          )}
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {!state && (
        <PoolScreen
          pool={pool}
          loading={poolLoading}
          error={poolError}
          genSeed={genSeed}
          setGenSeed={setGenSeed}
          genCount={genCount}
          setGenCount={setGenCount}
          genInternational={genInternational}
          setGenInternational={setGenInternational}
          onGenerate={generatePool}
          onStartAuction={startAuctionFromPool}
          onViewPlayer={showPlayerDetail}
          onOpenCreatePlayer={() => setCreatePlayerOpen(true)}
          onToggleShortlist={doTogglePoolShortlist}
          busy={busy}
        />
      )}

      {state && view === "summary" && (
        <>
          <GameSummary
            data={summary}
            loading={summaryLoading}
            error={summaryError}
            onViewPlayer={showPlayerDetail}
          />
          <ActivityFeed events={state.event_log} />
        </>
      )}

      {state && view === "auction" && (
        <div className="layout">
          <div className="column main-column">
            <PlayerCard
              player={state.current_player}
              onViewPlayer={showPlayerDetail}
              onToggleShortlist={doToggleShortlist}
            />
            <AuctionStatus state={state} onShowRemainingPlayers={showRemainingPlayers} />
            <Controls
              state={state}
              onBid={doBid}
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
          onViewStartingEleven={showStartingEleven}
          onViewPlayer={showPlayerDetail}
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
          onViewPlayer={showPlayerDetail}
          onToggleShortlist={doToggleShortlist}
        />
      )}

      {startingElevenOpen && (
        <StartingElevenModal
          data={startingEleven}
          loading={startingElevenLoading}
          error={startingElevenError}
          onClose={() => {
            setStartingElevenOpen(false);
            setStartingEleven(null);
          }}
        />
      )}

      {playerDetailOpen && (
        <PlayerDetailModal
          data={playerDetail}
          loading={playerDetailLoading}
          error={playerDetailError}
          onClose={() => {
            setPlayerDetailOpen(false);
            setPlayerDetail(null);
          }}
        />
      )}

      {createPlayerOpen && (
        <CreatePlayerScreen
          poolId={pool?.pool_id}
          onClose={() => setCreatePlayerOpen(false)}
          onPlayerAdded={refreshPoolAfterCustomPlayer}
        />
      )}
    </div>
  );
}
