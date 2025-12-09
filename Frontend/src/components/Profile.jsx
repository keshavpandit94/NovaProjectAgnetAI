// src/components/Profile.jsx
import React, { useState, useEffect } from 'react';
import { Mail, User, Calendar, CornerDownRight, LogOut, CheckCircle } from 'lucide-react';

const API_BASE_URL = "http://127.0.0.1:8001/api/v1";

const ProfileDetail = ({ icon: Icon, label, value }) => (
    <div className="flex items-center space-x-4 p-3 bg-slate-800 rounded-lg border border-slate-700">
      <Icon size={20} className="text-indigo-400" />
      <div>
        <p className="text-sm text-slate-400">{label}</p>
        <p className="text-lg font-medium text-slate-100">{value}</p>
      </div>
    </div>
);

const Profile = ({ userToken, onLogout }) => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userToken) return;

    const fetchProfile = async () => {
        try {
            // ... (API call setup remains the same)
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${userToken}`,
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log(data)

            if (!response.ok) {
                setError(data.detail || "Failed to fetch user profile.");
                setLoading(false);
                return;
            }
            
            setProfile({
                username: data.username || 'N/A',
                name: data.name || 'N/A',
                email: data.email || 'N/A',
                dob: data.dob ? new Date(data.dob).toLocaleDateString() : 'N/A',
                memberSince: data.memberSince ? new Date(data.memberSince).toLocaleDateString() : 'N/A',
            });
            setLoading(false);

        } catch (err) {
            setError("Network error while fetching profile.");
            setLoading(false);
        }
    };
    
    fetchProfile();
  }, [userToken]);


  if (loading) {
    return (
      <div className="flex-1 p-8 text-center text-slate-400">
        <p className="flex items-center justify-center space-x-2">
          <CornerDownRight size={20} className="animate-spin" />
          <span>Loading Profile...</span>
        </p>
      </div>
    );
  }

  if (error || !profile) {
    return <div className="flex-1 p-8 text-center text-red-400">Error: {error || 'No profile data available.'}</div>;
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 **bg-slate-800**"> {/* ✅ Profile background updated */}
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center border-b border-slate-700 pb-4 mb-8">
          <h2 className="text-4xl font-extrabold text-slate-100">User Profile</h2>
          <button
            onClick={onLogout}
            className="flex items-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition duration-200"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2 p-6 bg-custom-card border border-slate-700 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4 text-indigo-400 flex items-center space-x-2">
              <CheckCircle size={20} />
              <span>Account Information</span>
            </h3>
            <div className="space-y-4">
                <ProfileDetail icon={User} label="Username" value={profile.username} />
                <ProfileDetail icon={Mail} label="Email Address" value={profile.email} />
                <ProfileDetail icon={User} label="Full Name" value={profile.name} />
            </div>
          </div>
          
          <ProfileDetail icon={Calendar} label="Date of Birth" value={profile.dob} />
          <ProfileDetail icon={CornerDownRight} label="Member Since" value={profile.memberSince} />
        </div>
      </div>
    </div>
  );
};

export default Profile;