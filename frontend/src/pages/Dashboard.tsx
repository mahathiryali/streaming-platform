import { useState, useEffect, useRef } from "react"
import VideoCard from "../components/VideoCard"

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
    const [continueWatching, setContinueWatching] = useState<any[]>([]);
    const [isLoading, setIsLoading ] = useState(true)
    const [isLoaded, setIsLoaded] = useState(false);
    const [selectedVideo, setSelectedVideo] = useState<ContentItem | null>(null);
    const videoRef = useRef<HTMLVideoElement>(null);
    const [favorites, setFavorites] = useState<number[]>([]);
    const [recommended, setRecommended] = useState<ContentItem[]>([]);

    useEffect(() => {
        const video = videoRef.current;
        const startPosition = (selectedVideo as any)?.position_seconds;
    
        if (selectedVideo && video && startPosition > 0) {
            const handleMetadata = () => {
                video.currentTime = startPosition;
            };
    
            if (video.readyState >= 1) {
                handleMetadata();
            } else {
                video.addEventListener('loadedmetadata', handleMetadata);
                return () => video.removeEventListener('loadedmetadata', handleMetadata);
            }
        }
    }, [selectedVideo, videoRef.current]);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const headers = { "Authorization": `Bearer ${token}` };
        fetch("http://localhost:8000/content")
            .then(res => res.json())
            .then(data => {
                setVideos(data)
                setIsLoading(false)
                })
            .catch(err => console.error("Error fetching:", err));
        fetch("http://localhost:8000/users/me/continue_watching", { headers })
            .then(res => res.json())
            .then(data => setContinueWatching(data))
            .catch(err => console.error("Error fetching progress:", err));
            
    }, []);

    useEffect(() => {
        const token = localStorage.getItem('token');
        fetch("http://localhost:8000/users/me/favorites", {
            headers: { "Authorization": `Bearer ${token}` }
        })
        .then(res => res.json())
        .then(data => setFavorites(data.map((f: any) => f.content_id)));
    }, []);

    useEffect(() => {
        const token = localStorage.getItem('token');
        fetch("http://localhost:8000/videos/recommended", {
            headers: { "Authorization": `Bearer ${token}` }
        })
        .then(res => res.json())
        .then(data => setRecommended(data));
    }, [favorites]);
    

    if (isLoading) return <div className="p-8 text-white">Loading your library...</div>

    const sendPlaybackEvent = async (currentTime: number, eventType: string) => {
        const token = localStorage.getItem('token');
        if (!selectedVideo || !token) return;
    
        await fetch("http://localhost:8000/playback/event", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                content_id: selectedVideo.id,
                position_seconds: Math.floor(currentTime),
                event_type: eventType,
                device_id: "web_browser",
                session_id: "85829631-016f-4091-881c-f230f5763567",
                client_timestamp: new Date().toISOString()
            })
        });
    };

    
    const toggleFavorite = async (e: React.MouseEvent, contentId: number) => {
        e.stopPropagation();
        const token = localStorage.getItem('token');
    
        const response = await fetch(`http://localhost:8000/content/${contentId}/favorite`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        });
    
        if (response.ok) {
            setFavorites(prev => 
                prev.includes(contentId) 
                    ? prev.filter(id => id !== contentId) 
                    : [...prev, contentId]
            );
        }
    };

    return (
        
        <div className="p-6 bg-gray-900 min-h-screen">
            {continueWatching.length > 0 && (
                <section className="mb-12">
                    <h2 className="text-white text-2xl font-bold mb-4">Continue Watching</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                        {continueWatching.map((item, index) => {
                            const uniqueId = item.id || item.content?.id || index;
                            const videoData = item.content || item;
                            
                            return (
                                <div 
                                    key={`continue-${uniqueId}`} 
                                    onClick={() => {
                                        const videoData = item.content || item;
                                        console.log("Playing Video Data:", videoData);
                                        setSelectedVideo({ 
                                            ...videoData, 
                                            position_seconds: item.position_seconds 
                                        });
                                    }}
                                    className="group cursor-pointer"
                                >
                                    <div className="relative aspect-video rounded-lg overflow-hidden bg-gray-800 animate-pulse">
                                        <img 
                                            src={videoData.thumbnail_url} 
                                            alt={videoData.title} 
                                            className="w-full h-full object-cover opacity-0 transition-opacity duration-500"
                                            onClick={() => console.log(videoData.thumbnail_url)}
                                            onLoad={(e) => {
                                                e.currentTarget.classList.remove("opacity-0");
                                                e.currentTarget.classList.add("opacity-100");
                                                e.currentTarget.parentElement?.classList.remove("animate-pulse");
                                            }}
                                        />
                                        <div className="absolute bottom-0 left-0 h-1.5 bg-gray-600/50 w-full">
                                            <div 
                                                className="h-full bg-red-600" 
                                                style={{ width: `${Math.min((item.position_seconds / videoData.duration_seconds) * 100, 100)}%` }}
                                            />
                                        </div>
                                    </div>
                                    <h3 className="text-white text-sm mt-2 truncate">{videoData.title}</h3>
                                </div>
                            );
                        })}
                    </div>
                </section>
            )}

            {favorites.length > 0 && (
                <section className="mb-12">
                    <h2 className="text-white text-2xl font-bold mb-4 flex items-center gap-2">
                        <span>❤️</span> Your Favorites
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                        {videos.filter(v => favorites.includes(v.id)).map((item) => (
                            <div key={`fav-${item.id}`} onClick={() => setSelectedVideo(item)} className="cursor-pointer">
                                <div className="aspect-video rounded-lg overflow-hidden border-2 border-transparent hover:border-red-500 transition-all">
                                    <img src={item.thumbnail_url} className="w-full h-full object-cover" />
                                </div>
                                <h3 className="text-white text-sm mt-2 truncate">{item.title}</h3>
                            </div>
                        ))}
                    </div>
                </section>
            )}
                <section className="mb-12">
                            <h2 className="text-white text-2xl font-bold mb-4">Recommended for You</h2>
                            <div className="grid grid-cols-5 gap-4">
                                {recommended.map(video => (
                                    <VideoCard 
                                    key={`rec-${video.id}`} 
                                    item={video} 
                                    isFavorited={favorites.includes(video.id)}
                                    toggleFavorite={toggleFavorite}
                                    setSelectedVideo={setSelectedVideo}
                                />
                                ))}
                            </div>
                        </section>

            <h2 className="text-white text-2xl font-bold mb-4">More Content</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {videos.map((item) => {
                    // Check if this specific video ID is in our favorites state
                    const isFavorited = favorites.includes(item.id);

                    return (
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
                                />
                            </div>

                            <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                                
                                <button 
                                    onClick={(e) => toggleFavorite(e, item.id)}
                                    className="absolute top-2 right-2 p-2 rounded-full bg-black/40 hover:bg-black/60 transition-all opacity-0 group-hover:opacity-100 z-30"
                                    title={isFavorited ? "Remove from Favorites" : "Add to Favorites"}
                                >
                                    <svg 
                                        xmlns="http://www.w3.org/2000/svg" 
                                        fill={isFavorited ? "currentColor" : "none"} 
                                        viewBox="0 0 24 24" 
                                        strokeWidth={1.5} 
                                        stroke="currentColor" 
                                        className={`w-6 h-6 transition-colors ${isFavorited ? 'text-red-500' : 'text-white'}`}
                                    >
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                                    </svg>
                                </button>
                                <div className="pointer-events-none">
                                    <h3 className="text-white font-semibold text-sm truncate">{item.title}</h3>
                                    <p className="text-gray-300 text-xs line-clamp-2">{item.description}</p>
                                </div>
                                <span className="text-green-400 text-xs mt-2 font-mono">
                                    {Math.floor(item.duration_seconds / 60)}:{(item.duration_seconds % 60).toString().padStart(2, '0')}
                                </span>
                            </div>
                        </div>
                    );
                })}
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
                            ref={videoRef}
                            src={selectedVideo.video_url} 
                            controls 
                            autoPlay
                            onTimeUpdate={(e) => {
                                if (Math.floor(e.currentTarget.currentTime) % 10 === 0) {
                                    sendPlaybackEvent(e.currentTarget.currentTime, "heartbeat");
                                }
                            }}
                            onPause={(e) => sendPlaybackEvent(e.currentTarget.currentTime, "pause")} 
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