import { useState, useEffect } from "react"

interface ContentItem {
    id: number
    title: string
    description: string
    video_url: string
    thumbnail_url: string
    duration_seconds: number
    created_at: Date
}

function Dashboard() {
    const [videos, setVideos] = useState<ContentItem[]>([]);
    const [isLoading, setIsLoading ] = useState(true)
    const [isLoaded, setIsLoaded] = useState(false);
    const [selectedVideo, setSelectedVideo] = useState<ContentItem | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/content")
            .then(res => res.json())
            .then(data => {
                setVideos(data)
                setIsLoading(false)
                })
            .catch(err => console.error("Error fetching:", err));
    }, []);

    if (isLoading) return <div className="p-8 text-white">Loading your library...</div>

    return (
        
        <div className="p-6 bg-gray-900 min-h-screen">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {videos.map((item) => (
                    <div key={item.id} className="group relative bg-gray-800 rounded-lg overflow-hidden transition-transform duration-300 hover:scale-105 hover:z-10 cursor-pointer shadow-lg" onClick={() => setSelectedVideo(item)}>
                        <div className={`aspect-video bg-gray-800 rounded-lg ${!isLoaded ? 'animate-pulse' : ''}`}>
                            <img 
                                src={item.thumbnail_url} 
                                alt={item.title} 
                                className={`w-full h-full object-cover transition-opacity duration-500 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
                                onLoad={(e) => {
                                    e.currentTarget.classList.replace("opacity-0", "opacity-100");
                                    e.currentTarget.parentElement?.classList.remove("animate-pulse");
                                }}
                                onError={(e) => {
                                    e.currentTarget.parentElement?.classList.remove("animate-pulse");
                                    console.error("Image failed to load:", item.thumbnail_url);
                                }}
                            />
                        </div>

                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                            <h3 className="text-white font-semibold text-sm truncate">{item.title}</h3>
                            <p className="text-gray-300 text-xs line-clamp-2">{item.description}</p>
                            <span className="text-green-400 text-xs mt-2 font-mono">
                                {Math.floor(item.duration_seconds / 60)}:{(item.duration_seconds % 60).toString().padStart(2, '0')}
                            </span>
                        </div>

                    </div>
                ))}
            </div>
            {selectedVideo && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4 animate-in fade-in duration-300">
                    <button 
                        onClick={() => setSelectedVideo(null)}
                        className="absolute top-6 right-6 text-white text-4xl hover:text-gray-400 z-50"
                    >
                        &times;
                    </button>

                    <div className="w-full max-w-5xl aspect-video bg-black shadow-2xl rounded-lg overflow-hidden">
                        <video 
                            src={selectedVideo.video_url} 
                            controls 
                            autoPlay 
                            className="w-full h-full"
                        />
                        <div className="p-4 bg-gray-900">
                            <h2 className="text-xl font-bold text-white">{selectedVideo.title}</h2>
                            <p className="text-gray-400 mt-1">{selectedVideo.description}</p>
                        </div>
                    </div>
                </div>
            )

            }
        </div>
    )
}

export default Dashboard