import { useState } from "react"
import { useNavigate } from 'react-router-dom';

function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    
    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }
    
        try {
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
            
            if (response.ok) {
                navigate("/login");
            } else {
                setError("Registration failed. Email might be taken.");
            }
        } catch (err) {
            setError("Server connection failed");
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-900">
            <form onSubmit={handleRegister} className="bg-black/75 p-10 rounded-lg w-96 shadow-2xl">
                <h1 className="text-white text-3xl font-bold mb-6">Sign Up</h1>
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
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full p-3 mb-4 bg-gray-700 text-white rounded focus:outline-none focus:ring-2 ${
                        confirmPassword && password !== confirmPassword ? 'ring-2 ring-orange-500' : 'focus:ring-red-600"
                    required
                />
                <button className="w-full py-3 bg-red-600 text-white font-bold rounded hover:bg-red-700 transition cursor-pointer">Create Account</button>
            </form>

        </div>
    )
}

export default Register