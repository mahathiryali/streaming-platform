import { 
    HomeIcon, 
    InboxIcon, 
    PlayIcon, 
    MagnifyingGlassIcon, 
    Cog6ToothIcon, 
    ArrowLeftEndOnRectangleIcon,
    BoltIcon
  } from '@heroicons/react/24/outline';

import { useNavigate } from 'react-router-dom';

  const navigation = [
    { name: 'Home', href: '/home', icon: HomeIcon },
    { name: 'My Library', href: '/library', icon: InboxIcon },
    { name: 'Continue Watching', href: '/continue', icon: PlayIcon },
    { name: 'Browse', href: '/browse', icon: MagnifyingGlassIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
  ];

  interface UserProps {
    user: {
      name: string;
      email: string;
    };
  }

function Sidebar({user}: UserProps) {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
        window.location.reload();
    }

    return (
        <div className="flex h-screen w-64 flex-col bg-slate-900 text-white">
            <div className="flex h-20 items-center justify-center border-b border-slate-800">
                <h1 className="group flex items-center text-2xl font-bold text-indigo-500"><BoltIcon className="mr-3 h-6 w-6 flex-shrink-0" aria-hidden="true" />Streamify</h1>
            </div>

            <nav className="flex-1 space-y-1 px-4 py-4">
                {navigation.map((item) => (
                <a
                    key={item.name}
                    href={item.href}
                    className="group flex items-center rounded-md px-3 py-2 text-sm font-medium hover:bg-slate-800 hover:text-indigo-400 transition-colors"
                >
                    <item.icon className="mr-3 h-6 w-6 flex-shrink-0" aria-hidden="true" />
                    {item.name}
                </a>
                ))}
                <a
                    key="Log Out"
                    onClick={handleLogout}
                    className="group flex items-center rounded-md px-3 py-2 text-sm font-medium text-red-500 hover:bg-slate-800 hover:text-red-400 transition-colors cursor-pointer"
                >
                    <ArrowLeftEndOnRectangleIcon className="mr-3 h-6 w-6 flex-shrink-0" aria-hidden="true"/>
                    Log Out
                </a>
            </nav>

            <div className="border-t border-slate-800 p-4">
                <a href="/account" className="group block flex-shrink-0">
                <div className="flex items-center">
                    <div className="inline-block h-9 w-9 overflow-hidden rounded-full bg-slate-700">
                        {/* Default Avatar */}
                        <svg className="h-full w-full text-slate-300" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </div>
                    <div className="ml-3">
                    <p className="text-sm font-medium text-white group-hover:text-indigo-400 transition-colors">
                        {user?.name || 'User Name'}
                    </p>
                    <p className="text-xs font-medium text-slate-400 group-hover:text-slate-300">
                        {user?.email}
                    </p>
                    </div>
                </div>
                </a>
            </div>
        </div>
    )
  }
  
  export default Sidebar