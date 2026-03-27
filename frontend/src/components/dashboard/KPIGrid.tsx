export default function KPIGrid({ summary }: any) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
      {Object.entries(summary).map(([key, value]) => (
        <div key={key} style={card}>
          <strong>{key.toUpperCase()}</strong>
          <p>{value}</p>
        </div>
      ))}
    </div>
  );
}

const card = {
  border: "1px solid #ddd",
  padding: 12,
};