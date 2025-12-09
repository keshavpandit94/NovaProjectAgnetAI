import { Plus, MessageSquare, Settings, User, LogOut, X } from 'lucide-react';
import React, { useState } from 'react';

const Sidebar = ({ onLogout, setCurrentView, currentView }) => {
  const [isOpen, setIsOpen] = useState(false); 

  // Simplified Nav Items for demonstration
  const navItems = [
    { icon: MessageSquare, name: "Today's Chat", view: 'chat' },
    // Profile is handled separately below
  ];

  const getNavLinkClass = (viewName) => (
      `w-full text-left flex items-center space-x-3 p-2 rounded-lg transition duration-150 
       ${currentView === viewName ? 'bg-slate-700 text-slate-100 font-semibold' : 'text-slate-300 hover:bg-slate-700'}`
  );

  return (
    <>
      {/* Mobile Menu Button (uses bg-slate-900) */}
      <button 
        className="lg:hidden fixed top-4 left-4 z-40 p-2 bg-slate-900 rounded-lg border border-slate-700 text-slate-300"
        onClick={() => setIsOpen(true)}
      >
        <Plus size={24} />
      </button>

      {/* Sidebar Content */}
      <div 
        className={`flex flex-col justify-between w-64 h-full bg-custom-card border-r border-slate-700 p-4 
                   fixed inset-y-0 left-0 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} 
                   lg:relative lg:translate-x-0 transition-transform duration-300 ease-in-out z-30`}
      >
        
        {/* Close Button for Mobile */}
        <button 
            className="absolute top-4 right-4 lg:hidden text-slate-400 hover:text-white"
            onClick={() => setIsOpen(false)}
        >
            <X size={24} />
        </button>

        {/* Top Section */}
        <div>
          <h1 className="text-xl font-bold text-slate-100 mb-6">AI Agent</h1>
          
          {/* New Chat Button / Primary Link */}
          <button
            onClick={() => setCurrentView('chat')} 
            className="w-full flex items-center justify-center p-3 mb-6 space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition duration-200 shadow-lg"
          >
            <Plus size={20} />
            <span>New Chat</span>
          </button>

          {/* Recent Chats History (Placeholder links) */}
          <nav className="space-y-2">
            <p className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">History</p>
            {navItems.map((item, index) => (
              <button
                key={index}
                // Assuming all history links go back to the chat view for simplicity
                onClick={() => setCurrentView('chat')} 
                className={`w-full text-left flex items-center space-x-3 p-2 rounded-lg text-slate-300 hover:bg-slate-700 transition duration-150 ${index === 0 ? 'bg-slate-700' : ''}`}
              >
                <item.icon size={16} />
                <span className="truncate">{item.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Bottom Section: Settings, Profile & Logout */}
        <div className="space-y-2 border-t border-slate-700 pt-4">
          
          {/* PROFILE LINK */}
          <button 
             onClick={() => setCurrentView('profile')}
             className={getNavLinkClass('profile')}
          >
            <User size={18} />
            <span>Profile</span>
          </button>
          
          <a href="#" className="flex items-center space-x-3 p-2 rounded-lg text-slate-300 hover:bg-slate-700 transition duration-150">
            <Settings size={18} />
            <span>Settings</span>
          </a>
          
          {/* LOGOUT BUTTON */}
          <button onClick={onLogout} className="w-full text-left flex items-center space-x-3 p-2 rounded-lg text-red-400 hover:bg-slate-700 transition duration-150">
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </div>
      
      {/* Overlay for mobile */}
      {isOpen && <div onClick={() => setIsOpen(false)} className="fixed inset-0 bg-black/50 lg:hidden z-20"></div>}
    </>
  );
};

export default Sidebar;