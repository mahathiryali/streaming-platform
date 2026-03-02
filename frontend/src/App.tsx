import Sidebar from "./components/Sidebar"
import Dashboard from "./pages/Dashboard"
import { Routes, Route, Navigate, Outlet, BrowserRouter } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { useEffect, useState } from "react";

const ProtectedRoute = () => {
  const token = localStorage.getItem('token');
  return token ? <Outlet /> : <Navigate to="/login" replace />;
};

function App() {
  const [user, setUser] = useState({ name: "Guest", email: "" })
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
        fetch("http://localhost:8000/users/me", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            setUser({ name: data.email.split('@')[0], email: data.email });
        })
        .catch(() => localStorage.removeItem('token'));
    }
  }, []);
  
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/home" element={
            <div className="flex min-h-screen bg-black">
              <aside className="w-64 fixed inset-y-0 flex-shrink-0">
                <Sidebar user={user} />
              </aside>

              <main className="flex-1 ml-64 p-8 text-white">
                <h2 className="text-3xl font-bold pb-4">Welcome, {user.name}!</h2>
                <Dashboard/>
              </main>
            </div>
          } />
        </Route>

        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App