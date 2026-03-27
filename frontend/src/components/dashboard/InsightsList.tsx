export default function InsightsList({ insights }: any) {
  return (
    <div style={{ marginTop: 24 }}>
      <h2>Insights</h2>
      {insights.map((i: any, index: number) => (
        <div key={index} style={card}>
          {i.message}
        </div>
      ))}
    </div>
  );
}

const card = {
  border: "1px solid #eee",
  padding: 10,
  marginBottom: 8,
};