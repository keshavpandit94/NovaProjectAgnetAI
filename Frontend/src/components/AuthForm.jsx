import React, { useState, useEffect } from 'react';
import { Mail, User, Lock, Calendar, CornerUpRight, Plus, LogIn, X } from 'lucide-react';
import BackendAPI from '../utils/api';

const API_BASE_URL = `https://novaprojectagnetaibackend.onrender.com/api/v1`;

const initialFormData = {
    email: '',
    password: '',
    username: '',
    name: '',
    dob: '',
};

const InputField = React.memo(({ icon: Icon, name, type = 'text', placeholder, required = true, formData, handleChange }) => (
    <div className="relative">
      <Icon size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" />
      <input
        type={type}
        name={name}
        value={formData[name] || ''} 
        onChange={handleChange}
        placeholder={placeholder}
        required={required}
        className="w-full p-3 pl-10 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150"
      />
    </div>
));


const AuthForm = ({ isLoginView: initialIsLogin, onAuthSuccess, onClose, onToggleView }) => {
  const [isLogin, setIsLogin] = useState(initialIsLogin);
  const [formData, setFormData] = useState(initialFormData);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setIsLogin(initialIsLogin);
  }, [initialIsLogin]);

  useEffect(() => {
    setFormData(initialFormData);
    setError(null);
  }, [isLogin]);


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleToggle = () => {
    setIsLogin(!isLogin);
    if (onToggleView) onToggleView();
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const endpoint = isLogin ? `${API_BASE_URL}/auth/login` : `${API_BASE_URL}/auth/signup`;
    
    let body;
    let headers = {};

    if (isLogin) {
        // Login requires x-www-form-urlencoded format for OAuth2PasswordRequestForm
        const urlEncodedData = new URLSearchParams();
        urlEncodedData.append('username', formData.email); // FastAPI expects 'username' (which is the email)
        urlEncodedData.append('password', formData.password);
        body = urlEncodedData;
        headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else {
        // Signup requires JSON format
        body = JSON.stringify({
            email: formData.email,
            password: formData.password,
            username: formData.username,
            name: formData.name || undefined,
            dob: formData.dob || undefined,
        });
        headers['Content-Type'] = 'application/json';
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: headers,
            body: body,
        });
        console.log(response)

        const data = await response.json();

        console.log(data)

        if (!response.ok) {
            setError(data.detail || `Error: ${response.statusText}`);
            return;
        }

        // Success: Store token (using localStorage for this example)
        localStorage.setItem('accessToken', data.access_token);
        
        if (onAuthSuccess) {
            onAuthSuccess({ token: data.access_token, user: formData.email });
        }
    } catch (err) {
        setError("Network error or server unreachable.");
    } finally {
        setLoading(false);
    }
  };


  return (
    <div className="fixed inset-0 flex justify-center items-center bg-slate-900 z-50">
      <div className="w-full max-w-lg p-8 bg-custom-card rounded-xl shadow-2xl border border-slate-700 relative">
        
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white transition duration-150">
             <X size={24} />
        </button>

        <h2 className="text-3xl font-bold text-slate-100 text-center mb-6">
          {isLogin ? 'Sign In' : 'Create Account'}
        </h2>
        
        {error && <p className="p-3 mb-4 bg-red-800 text-white rounded-lg text-center">{error}</p>}
        
        <form onSubmit={handleSubmit} className="space-y-4" key={isLogin ? 'login-form' : 'signup-form'}>
          
          <InputField icon={Mail} name="email" type="email" placeholder="Email Address" formData={formData} handleChange={handleChange} />
          <InputField icon={Lock} name="password" type="password" placeholder="Password" formData={formData} handleChange={handleChange} />
          
          {!isLogin && (
            <>
              <InputField icon={User} name="username" placeholder="Username" formData={formData} handleChange={handleChange} />
              <InputField icon={User} name="name" placeholder="Full Name (Optional)" required={false} formData={formData} handleChange={handleChange} />
              <InputField icon={Calendar} name="dob" type="date" placeholder="Date of Birth" required={false} formData={formData} handleChange={handleChange} />
            </>
          )}

          <button
            type="submit"
            className="w-full flex items-center justify-center p-3 mt-6 space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition duration-200 shadow-lg disabled:bg-indigo-400"
            disabled={loading}
          >
            {loading ? (
                <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    {isLogin ? 'Signing In...' : 'Registering...'}
                </>
            ) : isLogin ? (
              <><LogIn size={20} /><span>Sign In</span></>
            ) : (
              <><Plus size={20} /><span>Sign Up</span></>
            )}
          </button>
        </form>

        <p className="text-center text-sm text-slate-400 mt-6">
          {isLogin ? "Don't have an account?" : "Already have an account?"}
          <button
            onClick={handleToggle}
            className="text-indigo-400 hover:text-indigo-300 font-medium ml-1 inline-flex items-center"
            type="button"
            disabled={loading}
          >
            {isLogin ? (
              <><CornerUpRight size={16} className="mr-1" /> Sign Up</>
            ) : (
              <><CornerUpRight size={16} className="mr-1" /> Sign In</>
            )}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;