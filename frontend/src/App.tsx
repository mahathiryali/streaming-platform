import Sidebar from "./components/Sidebar"
import Dashboard from "./pages/Dashboard"

const userData = {name: "Maha R", email: "flast@gmail.com"}

function App() {
  return (
    <div className="flex min-h-screen bg-black">
      <aside className="w-64 fixed inset-y-0 flex-shrink-0">
        <Sidebar user={userData} />
      </aside>

      <main className="flex-1 ml-64 p-8 text-white">
        <h2 className="text-3xl font-bold">Welcome, {userData.name}!</h2>
        <Dashboard></Dashboard>
      </main>
    </div>
  )
}

export default App