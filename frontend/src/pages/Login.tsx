import { useState } from "react"
import { useNavigate } from 'react-router-dom';

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    
    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        try {
            const response = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem("token", data.access_token);
                navigate("/home")
            }
        } catch (err) {
            setError("Authentication failed");
        }
    };
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900">
            <form onSubmit={handleLogin} className="bg-black/75 p-10 rounded-lg w-96 shadow-2xl">
                <h1 className="text-white text-3xl font-bold mb-6">Sign In</h1>
                {error && <p className="text-red-500 mb-4 text-sm">{error}</p>}
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full p-3 mb-4 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full p-3 mb-4 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 focus:ring-red-600"
                    required
                />
                <button className="w-full py-3 bg-red-600 text-white font-bold rounded hover:bg-red-700 transition cursor-pointer">Sign In</button>
            </form>

        </div>
    )
}

export default Login