import { useWrapped } from "./context/WrappedContext";

function App() {
  const metrics = useWrapped();

  if (!metrics) return <p className="text-center p-4">Loading wrapped data...</p>;

 return (
  <div className="flex items-center justify-center min-h-screen w-screen bg-gray-100">
    <div className="text-center p-6 max-w-xl w-full">
  <h1 className="text-4xl font-bold mb-4">📚 2024 Book Wrapped</h1>
  <p>Total Books: {metrics.totalBooks}</p>
  <p>Total Books Read: {metrics.totalBooksRead}</p>
  <p>Total Books Not Read: {metrics.totalBooksNotRead}</p>
  <p>Total Authors: {metrics.totalAuthors}</p>
  <p>Total Series: {metrics.totalSeries}</p>
  <p>Total Genres: {metrics.totalGenres}</p>
  <p>Total Pages Read: {metrics.totalPagesRead}</p> {/* Not present in JSON but may be added later */}
  <p>Total Thickness (in): {metrics.totalThicknessIn.toFixed(2)}</p>
  <p>Total Width (ft): {metrics.totalWidthFt.toFixed(2)}</p>
  <p>Total Height (in): {metrics.totalHeightIn.toFixed(2)}</p>
  <p>Total Height (ft): {metrics.totalHeightFt.toFixed(2)}</p>
  <p>Total Height in Space Needles: {metrics.totalHeightSpaceNeedles.toFixed(1)}</p>
  <p>Total Height in Miles: {metrics.totalHeightMiles.toFixed(2)}</p>
  <p>Total Height in 10Ks: {metrics.totalHeight10k.toFixed(2)}</p>
  <p>Total Spent: ${metrics.totalSpent.toFixed(2)}</p>
  <p>Average Spent Per Book: ${metrics.averageSpentPerBook.toFixed(2)}</p>
</div>
  </div>
);
}

export default App;