export default function SocialCard({ social }: any) {
  if (!social) return null;

  return (
    <div style={card}>
      <h2>Social Metrics</h2>
      <p>Followers: {social.followers}</p>
      <p>Engagement: {social.engagement}</p>
      <p>Posts: {social.posts}</p>
      <p>Growth: {social.growth_rate}%</p>
    </div>
  );
}

const card = {
  border: "1px solid #ccc",
  padding: 16,
  marginTop: 24,
};