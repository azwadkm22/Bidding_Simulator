import { useEffect, useMemo, useRef, useState } from "react";
import * as api from "./api";
import "./App.css";

const POLL_MS = 1000;

function PlayerCard({ player, onViewPlayer }) {
  if (!player) return <div className="panel">No player on the block.</div>;
  return (
    <div className="panel">
      <h2>
        {player.name}{" "}
        <button className="link-button" onClick={() => onViewPlayer(player.player_id)}>
          [View Stats]
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
  { key: "batting", label: "Batting" },
  { key: "bowling", label: "Bowling" },
  { key: "fielding", label: "Fielding" },
];

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
function PlayerTable({ players, extraColumns, emptyMessage, rowClassName, onViewPlayer }) {
  const [positionFilter, setPositionFilter] = useState("All");
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
  }, [players, positionFilter, statKey, statMin, sortKey, sortDir]);

  function toggleSort(key) {
    if (key === sortKey) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir(key === "name" || key === "position" ? "asc" : "desc");
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
          </tr>
        </thead>
        <tbody>
          {visiblePlayers.map((p) => (
            <tr key={p.player_id} className={rowClassName ? rowClassName(p) : undefined}>
              <td>
                {onViewPlayer ? (
                  <button className="link-button" onClick={() => onViewPlayer(p.player_id)}>
                    {p.name}
                  </button>
                ) : (
                  p.name
                )}
              </td>
              <td>{p.position}</td>
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
            </tr>
          ))}
          {visiblePlayers.length === 0 && (
            <tr>
              <td colSpan={columns.length}>{emptyMessage}</td>
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
              Budget: {team.budget} · Squad size: {team.squad_size}{" "}
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
          </>
        )}
      </div>
    </div>
  );
}

function PlayerListModal({ data, loading, error, onClose, onViewPlayer }) {
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
                    <td>{p.name}</td>
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
                    <td>{p.name}</td>
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

function PoolCategoryPicker({ pool, onViewPlayer }) {
  const [category, setCategory] = useState(ALL_PLAYERS_KEY);
  const [allPlayers, setAllPlayers] = useState(null);
  const [allPlayersLoading, setAllPlayersLoading] = useState(false);
  const [allPlayersError, setAllPlayersError] = useState(null);

  useEffect(() => {
    if (category !== ALL_PLAYERS_KEY || allPlayers) return;
    setAllPlayersError(null);
    setAllPlayersLoading(true);
    api
      .getPoolPlayers(pool.pool_id)
      .then((data) => setAllPlayers(data.players))
      .catch((err) => setAllPlayersError(err.message))
      .finally(() => setAllPlayersLoading(false));
  }, [category, pool.pool_id, allPlayers]);

  const players = category === ALL_PLAYERS_KEY ? allPlayers || [] : pool[category];

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
  onGenerate,
  onStartAuction,
  onViewPlayer,
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
          <button onClick={onGenerate} disabled={loading}>
            {pool ? "Generate Different Pool" : "Generate Players"}
          </button>
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

          <PoolCategoryPicker pool={pool} onViewPlayer={onViewPlayer} />
        </>
      )}
    </div>
  );
}

function AttributeGrid({ title, attributes }) {
  const entries = Object.entries(attributes || {});
  if (entries.length === 0) return null;
  return (
    <div className="attribute-section">
      <h4>{title}</h4>
      <div className="attribute-grid">
        {entries.map(([key, value]) => (
          <div key={key} className="attribute-cell">
            <span className="attribute-label">{key}</span>
            <span className="attribute-value">{Math.round(value)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function RatingBadge({ label, rating }) {
  if (!rating) return null;
  return (
    <div className="rating-badge">
      <span className="rating-badge-label">{label}</span>
      <span className="rating-badge-value">{rating.unavailable ? "-" : rating.displayed}</span>
    </div>
  );
}

function PlayerDetailModal({ data, loading, error, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{data ? data.name : "Loading..."}</h2>
          <button onClick={onClose}>Close</button>
        </div>
        {loading && <p>Loading player...</p>}
        {error && <p className="error-banner">{error}</p>}
        {data && (
          <>
            <p>
              {data.position} · Role: {data.role}
              {data.primary_bowling_style !== "none" ? ` (${data.primary_bowling_style})` : ""}
            </p>
            <div className="rating-badges">
              <RatingBadge label="Overall" rating={data.ratings.overall} />
              <RatingBadge label="Batting" rating={data.ratings.batting} />
              <RatingBadge label="Bowling" rating={data.ratings.paceBowling || data.ratings.spinBowling} />
              <RatingBadge label="Fielding" rating={data.ratings.fielding} />
              <RatingBadge label="Keeping" rating={data.ratings.wicketkeeping} />
              <RatingBadge label="Mentality" rating={data.ratings.mentality} />
            </div>

            <AttributeGrid title="Batting" attributes={data.attributes.batting} />
            <AttributeGrid title="Pace Bowling" attributes={data.attributes.paceBowling} />
            <AttributeGrid title="Spin Bowling" attributes={data.attributes.spinBowling} />
            <AttributeGrid title="Fielding" attributes={data.attributes.fielding} />
            <AttributeGrid title="Wicketkeeping" attributes={data.attributes.wicketkeeping} />
            <AttributeGrid title="Physical" attributes={data.attributes.physical} />
            <AttributeGrid title="Mentality" attributes={data.attributes.mentality} />
            {Object.entries(data.attributes.repertoire || {}).map(
              ([style, deliveries]) =>
                Object.keys(deliveries).length > 0 && (
                  <AttributeGrid
                    key={style}
                    title={`${style === "pace" ? "Pace" : "Spin"} Repertoire`}
                    attributes={deliveries}
                  />
                ),
            )}
            <AttributeGrid title="Traits" attributes={data.attributes.traits} />
            <AttributeGrid title="State" attributes={data.attributes.state} />
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
      const data = await api.generatePool({ seed: genSeed, count: genCount });
      setPool(data);
      setState(null);
      setSessionId(null);
    } catch (err) {
      setPoolError(err.message);
    } finally {
      setPoolLoading(false);
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
          onGenerate={generatePool}
          onStartAuction={startAuctionFromPool}
          onViewPlayer={showPlayerDetail}
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
            <PlayerCard player={state.current_player} onViewPlayer={showPlayerDetail} />
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
    </div>
  );
}
