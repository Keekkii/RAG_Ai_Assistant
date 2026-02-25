import React, { useState, useEffect } from "react";
import "./Dashboard.css";

const Dashboard = ({ onClose }) => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedLog, setSelectedLog] = useState(null);

    const fetchLogs = async () => {
        try {
            const response = await fetch("http://localhost:8000/logs");
            const data = await response.json();
            setLogs(data);
        } catch (error) {
            console.error("Error fetching logs:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs();
        const interval = setInterval(fetchLogs, 5000); // Auto refresh every 5s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="dashboard-overlay">
            <div className="dashboard-window">
                <header className="dashboard-header">
                    <div className="header-info">
                        <h2>Activity Dashboard</h2>
                        <span className="live-badge">LIVE</span>
                    </div>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </header>

                <div className="dashboard-content">
                    {loading ? (
                        <div className="loading-state">Loading logs...</div>
                    ) : logs.length === 0 ? (
                        <div className="empty-state">No activity logs found.</div>
                    ) : (
                        <div className="logs-table-container">
                            <table className="logs-table">
                                <thead>
                                    <tr>
                                        <th>Timestamp</th>
                                        <th>Query</th>
                                        <th>Latency</th>
                                        <th>Top Chunk</th>
                                        <th>RRF</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {logs.map((log, index) => (
                                        <tr
                                            key={index}
                                            className={`log-row ${selectedLog === log ? 'active' : ''}`}
                                            onClick={() => setSelectedLog(log)}
                                        >
                                            <td>{new Date(log.timestamp).toLocaleTimeString()}</td>
                                            <td className="query-cell" title={log.query}>{log.query}</td>
                                            <td>
                                                <span className={`latency-pill ${log.latency_ms > 10000 ? "slow" : "fast"}`}>
                                                    {(log.latency_ms / 1000).toFixed(1)}s
                                                </span>
                                            </td>
                                            <td className="chunk-cell">{log.retrieved_chunks?.[0]?.title || "N/A"}</td>
                                            <td className="score-cell">{log.retrieved_chunks?.[0]?.rrf_score?.toFixed(4) || "0.0000"}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                {selectedLog && (
                    <div className="json-viewer-overlay" onClick={() => setSelectedLog(null)}>
                        <div className="json-viewer-content" onClick={e => e.stopPropagation()}>
                            <header className="viewer-header">
                                <h3>Raw Log View</h3>
                                <button onClick={() => setSelectedLog(null)}>&times;</button>
                            </header>
                            <pre>
                                {JSON.stringify(selectedLog, null, 2)}
                            </pre>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
