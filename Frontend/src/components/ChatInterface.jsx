import { Send, Camera, User, Zap } from 'lucide-react';
import React, { useState, useRef, useEffect } from 'react';
import BackendAPI from '../utils/api';

const API_BASE_URL = `${BackendAPI}/api/v1`;

const ChatInterface = ({ userToken }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const isAnonymous = !userToken;

  useEffect(() => {
    setMessages([]); 
  }, [userToken]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() && !imageFile) return;

    const userMessage = { 
        type: 'user', 
        text: inputText.trim(), 
        image: imageFile ? URL.createObjectURL(imageFile) : null, 
        icon: User 
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText.trim();
    setInputText('');
    setImageFile(null);
    setLoading(true);

    // --- API CALL SETUP (Removed for brevity - Logic is unchanged) ---
    const formData = new FormData();
    formData.append('user_input_text', currentInput);
    
    if (imageFile) {
        formData.append('image_file', imageFile);
    }

    const headers = {};
    if (!isAnonymous) {
        headers['Authorization'] = `Bearer ${userToken}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/chat/`, {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        const data = await response.json();
        // const data = response;

        console.log(data)
        if (!response.ok) {
            setMessages(prev => [...prev, { type: 'error', text: data.detail || "An API error occurred.", icon: Zap }]);
            return;
        }
        
        const aiMessage = { 
            type: 'ai', 
            text: data.ai_response, 
            icon: Zap 
        };
        
        setMessages(prev => [...prev, aiMessage]);

    } catch (err) {
        setMessages(prev => [...prev, { type: 'error', text: "Failed to connect to the server.", icon: Zap }]);
    } finally {
        setLoading(false);
    }
  };


  const MessageBubble = ({ msg }) => (
    <div className={`flex space-x-4 max-w-3xl ${msg.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
        
        <div className={`p-2 rounded-full h-fit ${msg.type === 'user' ? 'bg-indigo-600' : 'bg-slate-700'}`}>
          <msg.icon size={18} className="text-white" />
        </div>
        
        <div className={`p-4 rounded-xl shadow-lg ${
          msg.type === 'user' 
            ? 'bg-indigo-600 text-white rounded-br-none' 
            : 'bg-custom-card text-slate-200 rounded-tl-none border border-slate-700'
        }`}>
          {msg.image && (
              <img src={msg.image} alt="User Upload" className="mb-2 max-h-48 object-contain rounded-lg border border-slate-600" />
          )}
          <p>{msg.text}</p>
        </div>
    </div>
  );


  return (
    <div className="flex flex-col flex-1 h-full">
      {/* Message Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        {messages.length === 0 && (
            <div className='flex flex-col items-center justify-center h-full text-slate-400'>
                <Zap size={40} className='mb-4 text-indigo-500' />
                <h3 className='text-2xl font-bold mb-2'>Hello! How can I assist you?</h3>
                <p className='text-md'>I am ready to process your text and analyze your images.</p>
                {isAnonymous && <p className='text-sm mt-2 text-red-400'>Your search history will NOT be saved.</p>}
            </div>
        )}
        
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <MessageBubble msg={msg} />
          </div>
        ))}
        {loading && (
            <div className="flex justify-start">
                <div className="flex space-x-4 max-w-3xl">
                    <div className="p-2 rounded-full bg-slate-700 h-fit">
                        <Zap size={18} className="text-white" />
                    </div>
                    <div className="p-4 rounded-xl shadow-lg bg-custom-card text-slate-200 rounded-tl-none border border-slate-700">
                        <div className="flex items-center space-x-2">
                            <span className="text-slate-400">Thinking...</span>
                            <svg className="animate-spin h-5 w-5 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        </div>
                    </div>
                </div>
            </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={sendMessage} className="p-8 **bg-slate-800** border-t border-slate-700 sticky bottom-0"> {/* ✅ Input area background updated */}
        <div className="max-w-4xl mx-auto flex items-end">
          
          {/* Hidden File Input (omitted) */}
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept="image/*" 
            style={{ display: 'none' }} 
          />
          
          {/* File/Image Upload Button */}
          <button 
            type="button"
            onClick={() => fileInputRef.current.click()}
            className={`p-3 mr-4 text-slate-400 transition duration-150 rounded-full bg-custom-card border border-slate-700 ${imageFile ? 'text-indigo-400 ring-2 ring-indigo-500' : 'hover:text-indigo-400'}`}
          >
            <Camera size={20} />
          </button>

          {/* Text Input */}
          <textarea
            className="flex-1 min-h-[50px] max-h-40 p-3 **bg-custom-card** border border-slate-700 text-slate-200 rounded-xl resize-none focus:ring-indigo-500 focus:border-indigo-500 outline-none placeholder:text-slate-500"
            placeholder={imageFile ? `Image selected: ${imageFile.name}. Add a prompt...` : "Message AI Agent..."}
            rows={1}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onInput={(e) => {
              e.target.style.height = 'auto';
              e.target.style.height = (e.target.scrollHeight) + 'px';
            }}
            disabled={loading}
          />

          {/* Send Button (omitted) */}
          <button
            type="submit"
            className="p-3 ml-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition duration-200 disabled:bg-indigo-400"
            disabled={loading || (!inputText.trim() && !imageFile)}
          >
            <Send size={20} />
          </button>
        </div>
        <p className="text-center text-xs text-slate-500 mt-2">
          {imageFile && !loading && (
             <span className="text-indigo-400 mr-2">File Ready: {imageFile.name}</span>
          )}
          AI Agent can make mistakes. Consider checking important information.
        </p>
      </form>
    </div>
  );
};

export default ChatInterface;