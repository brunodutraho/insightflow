export default function Overview({ overview, score }: any) {
  if (score.available === false) {
    return (
      <div style={card}>
        <h2>Performance Score 🔒</h2>
        <p>{score.message}</p>
      </div>
    );
  }

  return (
    <div style={card}>
      <h2>Performance Score</h2>
      <h1>{overview.score}</h1>
      <p>{overview.status}</p>
    </div>
  );
}

const card = {
  border: "1px solid #ccc",
  padding: 16,
  marginBottom: 16,
};