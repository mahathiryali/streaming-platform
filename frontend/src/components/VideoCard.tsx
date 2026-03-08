interface VideoCardProps {
    item: any; 
    isFavorited: boolean;
    toggleFavorite: (e: React.MouseEvent, id: number) => void;
    setSelectedVideo: (video: any) => void;
}

const VideoCard = ({ item, isFavorited, toggleFavorite, setSelectedVideo }: VideoCardProps) => {
    return (
        <div 
            className="group relative bg-gray-800 rounded-lg overflow-hidden transition-transform duration-300 hover:scale-105 hover:z-10 cursor-pointer shadow-lg" 
            onClick={() => setSelectedVideo(item)}
        >
            <div className="aspect-video bg-gray-800 relative">
                <img 
                    src={item.thumbnail_url} 
                    alt={item.title} 
                    className="w-full h-full object-cover"
                />
                
                <button 
                    onClick={(e) => toggleFavorite(e, item.id)}
                    className="absolute top-2 right-2 p-2 rounded-full bg-black/40 hover:bg-black/60 transition-all opacity-0 group-hover:opacity-100 z-30"
                >
                    <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        fill={isFavorited ? "red" : "none"} 
                        viewBox="0 0 24 24" 
                        strokeWidth={2} 
                        stroke={isFavorited ? "red" : "white"} 
                        className="w-5 h-5"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                    </svg>
                </button>
            </div>

            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-4">
                <h3 className="text-white font-semibold text-sm truncate pr-10">
                    {item.title}
                </h3>
                <p className="text-gray-300 text-xs line-clamp-2 mt-1">
                    {item.description}
                </p>
            </div>
        </div>
    )
}

export default VideoCard