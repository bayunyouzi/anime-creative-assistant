import re

def redesign_ui():
    with open('app/page.tsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start of the return statement
    return_index = content.find('  return (\n    <main')
    if return_index == -1:
        return_index = content.find('  return (\n')
        
    if return_index == -1:
        print("Could not find return statement")
        return

    top_logic = content[:return_index]

    new_ui = """  return (
    <main className="min-h-screen bg-[#000000] text-zinc-100 font-sans selection:bg-indigo-500/30 overflow-hidden relative pb-20">
      {/* Dynamic Background */}
      <div className="fixed top-[-20%] left-[-10%] w-[60%] h-[60%] rounded-full bg-indigo-900/20 blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[60%] h-[60%] rounded-full bg-rose-900/10 blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="absolute top-0 left-0 w-full h-full bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:64px_64px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none z-0" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 relative z-10 pt-6">
        {/* Header */}
        <header className="flex justify-between items-center mb-16 md:mb-24 bg-white/[0.02] border border-white/[0.05] rounded-2xl px-6 py-4 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-rose-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-black tracking-wider text-sm sm:text-base bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">PROMPT.STUDIO</h1>
              <p className="text-[10px] text-zinc-500 font-mono uppercase tracking-widest hidden sm:block">AI Creative Assistant</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2 sm:gap-4">
            <a 
              href="https://qm.qq.com/q/Q982XX0UAo" 
              target="_blank" 
              rel="noopener noreferrer"
              className="hidden sm:flex items-center gap-2 px-4 py-2 bg-zinc-900/50 hover:bg-zinc-800 border border-white/10 text-zinc-300 hover:text-white rounded-xl text-xs font-medium transition-all"
            >
              <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current" xmlns="http://www.w3.org/2000/svg">
                <path d="M11.984 0A12 12 0 0 0 0 12c0 2.057.534 4.024 1.488 5.753l-1.077 3.993a.5.5 0 0 0 .61.61l3.993-1.077A11.944 11.944 0 0 0 11.984 24c6.627 0 12-5.373 12-12s-5.373-12-12-12zM7.5 13.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm9 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
              </svg>
              交流群
            </a>
            <button 
              onClick={() => setShowSponsor(true)}
              className="p-2 text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 rounded-xl transition-all"
              title="赞助支持"
            >
              <Heart className="w-5 h-5 fill-current" />
            </button>
            <button 
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-zinc-400 hover:text-white hover:bg-white/10 rounded-xl transition-all"
              title="API 设置"
            >
              <Settings className="w-5 h-5" />
            </button>
            
            <div className="w-px h-6 bg-white/10 mx-1"></div>

            {user ? (
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 rounded-xl text-xs font-bold transition-all border border-rose-500/20"
              >
                <User className="w-4 h-4" />
                <span className="hidden sm:inline">{user.email.split('@')[0]}</span>
              </button>
            ) : (
              <button
                onClick={() => setShowAuthModal(true)}
                className="flex items-center gap-2 px-5 py-2 bg-white text-black hover:bg-zinc-200 rounded-xl text-xs font-bold transition-all shadow-[0_0_20px_rgba(255,255,255,0.2)]"
              >
                <User className="w-4 h-4" />
                登录 / 注册
              </button>
            )}
          </div>
        </header>

        {/* Hero Typography */}
        <div className="text-center mb-16 space-y-6">
          <h2 className="text-5xl md:text-7xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-zinc-500 drop-shadow-2xl">
            Redefine <br className="md:hidden" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-rose-400">Creation.</span>
          </h2>
          <p className="text-zinc-400 max-w-2xl mx-auto text-base md:text-lg font-light tracking-wide">
            突破想象边界。专业的二次元、写实及视频 AI 提示词生成与图生图引擎。
          </p>
          
          {!user && (
            <div className="flex flex-wrap justify-center gap-3 text-xs font-mono text-zinc-500 mt-4">
              <span className={`px-4 py-2 rounded-xl border bg-black/40 backdrop-blur-sm ${guestLimits.prompt > 0 ? 'border-indigo-500/30 text-indigo-400' : 'border-rose-500/30 text-rose-500'}`}>
                GUEST PROMPTS: {guestLimits.prompt}
              </span>
              <span className={`px-4 py-2 rounded-xl border bg-black/40 backdrop-blur-sm ${guestLimits.image > 0 ? 'border-indigo-500/30 text-indigo-400' : 'border-rose-500/30 text-rose-500'}`}>
                GUEST IMAGES: {guestLimits.image}
              </span>
            </div>
          )}
        </div>

        {/* Auth Modal (kept from original) */}
        <AuthModal 
          isOpen={showAuthModal} 
          onClose={() => setShowAuthModal(false)}
          onLoginSuccess={(token, userData) => {
            setUser(userData);
          }}
        />

        {/* Settings Panel */}
        {showSettings && (
          <div className="w-full bg-zinc-900/60 backdrop-blur-3xl border border-white/10 rounded-3xl p-6 md:p-10 mb-12 shadow-2xl animate-in fade-in slide-in-from-top-4 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-rose-500"></div>
            <div className="grid md:grid-cols-2 gap-10">
              {/* Prompt API */}
              <div className="space-y-5">
                <h3 className="text-lg font-bold flex items-center gap-2 text-indigo-400">
                  <Wand2 className="w-5 h-5" /> Prompt Engine API
                </h3>
                <p className="text-xs text-zinc-500">用于生成高质量的英文 Prompt。默认使用内置高速通道。</p>
                <div className="space-y-3">
                  <input type="text" value={apiEndpoint} onChange={(e) => setApiEndpoint(e.target.value)} placeholder="Endpoint (默认内置)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-colors" />
                  <input type="text" value={modelName} onChange={(e) => setModelName(e.target.value)} placeholder="Model (默认内置)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-colors" />
                  <input type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="API Key (默认内置)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-colors" />
                </div>
              </div>
              {/* Image API */}
              <div className="space-y-5">
                <h3 className="text-lg font-bold flex items-center gap-2 text-rose-400">
                  <ImageIcon className="w-5 h-5" /> Image Generation API
                </h3>
                <p className="text-xs text-zinc-500">用于实际生成图片。<span className="text-rose-400">填入自定义 Key 解除限制。</span></p>
                <div className="space-y-3">
                  <input type="text" value={imageApiEndpoint} onChange={(e) => setImageApiEndpoint(e.target.value)} placeholder="Endpoint (e.g. https://api...)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-rose-500 outline-none transition-colors" />
                  <input type="text" value={imageModelName} onChange={(e) => setImageModelName(e.target.value)} placeholder="Model (e.g. dall-e-3)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-rose-500 outline-none transition-colors" />
                  <input type="password" value={imageApiKey} onChange={(e) => setImageApiKey(e.target.value)} placeholder="API Key (sk-...)" className="w-full bg-black/50 border border-white/5 rounded-xl px-4 py-3 text-sm focus:border-rose-500 outline-none transition-colors" />
                </div>
              </div>
            </div>
            <div className="mt-8 flex justify-end">
              <button onClick={saveSettings} className="flex items-center gap-2 bg-white text-black px-8 py-3 rounded-xl font-bold transition-all hover:scale-95">
                <Save className="w-4 h-4" /> Save Configuration
              </button>
            </div>
          </div>
        )}

        {/* Main Workspace - Bento Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
          
          {/* Left Column: Mode Selector (4 cols) */}
          <div className="lg:col-span-4 flex flex-col gap-4">
            <div className="bg-white/[0.02] border border-white/[0.05] rounded-3xl p-3 backdrop-blur-xl flex flex-col gap-2 shadow-xl">
              <button
                onClick={() => { setIsAnime(true); setIsVideoMode(false); setIsImg2ImgMode(false); }}
                className={`flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 ${isAnime && !isVideoMode && !isImg2ImgMode ? 'bg-indigo-500/10 border border-indigo-500/30 text-indigo-300' : 'hover:bg-white/5 text-zinc-400 border border-transparent'}`}
              >
                <div className="flex items-center gap-3"><Sparkles className="w-5 h-5" /><span className="font-bold text-sm tracking-wide">二次元动漫</span></div>
                {isAnime && !isVideoMode && !isImg2ImgMode && <div className="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,1)]" />}
              </button>
              <button
                onClick={() => { setIsAnime(false); setIsVideoMode(false); setIsImg2ImgMode(false); }}
                className={`flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 ${!isAnime && !isVideoMode && !isImg2ImgMode ? 'bg-indigo-500/10 border border-indigo-500/30 text-indigo-300' : 'hover:bg-white/5 text-zinc-400 border border-transparent'}`}
              >
                <div className="flex items-center gap-3"><ImageIcon className="w-5 h-5" /><span className="font-bold text-sm tracking-wide">写实摄影</span></div>
                {!isAnime && !isVideoMode && !isImg2ImgMode && <div className="w-2 h-2 rounded-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,1)]" />}
              </button>
              <button
                onClick={() => { setIsVideoMode(true); setIsDeepThinking(true); setIsImg2ImgMode(false); }}
                className={`flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 ${isVideoMode && !isImg2ImgMode ? 'bg-purple-500/10 border border-purple-500/30 text-purple-300' : 'hover:bg-white/5 text-zinc-400 border border-transparent'}`}
              >
                <div className="flex items-center gap-3"><Video className="w-5 h-5" /><span className="font-bold text-sm tracking-wide">动态视频引擎</span></div>
                {isVideoMode && !isImg2ImgMode && <div className="w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,1)]" />}
              </button>
              <button
                onClick={() => { setIsImg2ImgMode(true); setIsVideoMode(false); setIsAnime(false); }}
                className={`flex items-center justify-between px-5 py-4 rounded-2xl transition-all duration-300 ${isImg2ImgMode ? 'bg-rose-500/10 border border-rose-500/30 text-rose-300' : 'hover:bg-white/5 text-zinc-400 border border-transparent'}`}
              >
                <div className="flex items-center gap-3"><ImageIcon className="w-5 h-5" /><span className="font-bold text-sm tracking-wide">AI 图生图</span></div>
                {isImg2ImgMode && <div className="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,1)]" />}
              </button>
            </div>

            {/* Sub-controls (Safe mode, Characters) */}
            {!isImg2ImgMode && (
              <div className="bg-white/[0.02] border border-white/[0.05] rounded-3xl p-5 backdrop-blur-xl space-y-5 shadow-xl">
                <div className="flex flex-col gap-3">
                  <button
                    onClick={() => setIsSafeMode(!isSafeMode)}
                    className={`flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-bold transition-all border ${isSafeMode ? "bg-white/5 border-white/10 text-zinc-300 hover:bg-white/10" : "bg-rose-500/10 border-rose-500/30 text-rose-400 shadow-[0_0_15px_rgba(244,63,94,0.15)]"}`}
                  >
                    {isSafeMode ? <Shield className="w-4 h-4" /> : <ShieldAlert className="w-4 h-4" />}
                    {isSafeMode ? "SAFE MODE: ON" : "CREATIVE MODE: UNLOCKED"}
                  </button>
                  <button
                    onClick={() => setIsDeepThinking(!isDeepThinking)}
                    disabled={isVideoMode}
                    className={`flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-bold transition-all border ${isDeepThinking || isVideoMode ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-400" : "bg-white/5 border-white/10 text-zinc-500"}`}
                  >
                    <Brain className="w-4 h-4" />
                    {isVideoMode ? "DEEP THINKING (LOCKED)" : (isDeepThinking ? "DEEP THINKING: ON" : "DEEP THINKING: OFF")}
                  </button>
                </div>
                
                {!isSafeMode && (
                  <p className="text-[10px] text-rose-400/80 text-center leading-relaxed font-mono">
                    WARNING: 创意模式已解锁。可能触发平台审查，若生成失败请重试或修改提示词。
                  </p>
                )}

                {!isVideoMode && (
                  <div className="bg-black/50 p-1.5 rounded-xl flex gap-1 border border-white/5">
                    {['default', 'solo', 'duo'].map(type => (
                      <button
                        key={type}
                        onClick={() => setCharacterCount(type as any)}
                        className={`flex-1 py-2 rounded-lg text-xs font-bold transition-all flex justify-center items-center gap-1 ${characterCount === type ? "bg-white/10 text-white shadow-sm" : "text-zinc-500 hover:text-zinc-300"}`}
                      >
                        {type === 'solo' && <User className="w-3 h-3" />}
                        {type === 'duo' && <Users className="w-3 h-3" />}
                        {type === 'default' ? 'MIXED' : type.toUpperCase()}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Right Column: Input & Actions (8 cols) */}
          <div className="lg:col-span-8 flex flex-col gap-6">
            <div className="bg-white/[0.02] border border-white/[0.05] rounded-[2rem] p-6 md:p-8 backdrop-blur-xl shadow-2xl relative min-h-[400px] flex flex-col">
              
              {!isImg2ImgMode ? (
                <div className="flex-1 flex flex-col justify-between">
                  <div className="mb-6">
                    <label className="text-xs font-mono text-zinc-500 mb-3 block uppercase tracking-widest">Base Concept / 中文扩写</label>
                    <textarea
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      placeholder="描述你想要的画面，例如：一个赛博朋克风格的少女站在霓虹街头，雨水打湿了她的衣服..."
                      className="w-full bg-black/40 border border-white/10 rounded-2xl px-6 py-5 text-sm text-zinc-200 placeholder-zinc-700 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none transition-all resize-none h-40 shadow-inner"
                    />
                  </div>
                  <button
                    onClick={handleGenerate}
                    disabled={loading}
                    className={`w-full py-5 rounded-2xl text-base md:text-lg font-black tracking-widest uppercase transition-all duration-300 flex items-center justify-center gap-3 relative overflow-hidden group ${loading ? "bg-zinc-800 text-zinc-500 cursor-wait" : "bg-white text-black hover:bg-zinc-200 hover:scale-[0.98] shadow-[0_0_40px_rgba(255,255,255,0.15)]"}`}
                  >
                    {loading ? <RefreshCw className="w-6 h-6 animate-spin" /> : <Wand2 className="w-6 h-6" />}
                    {loading ? "INITIALIZING..." : "GENERATE PROMPT"}
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-6 animate-in fade-in">
                  <div className="w-full h-64 border-2 border-dashed border-white/10 rounded-3xl flex flex-col items-center justify-center bg-black/20 hover:bg-black/40 hover:border-rose-500/50 transition-all duration-300 relative overflow-hidden group">
                    {uploadedImage ? (
                      <>
                        <img src={uploadedImage} alt="Uploaded" className="h-full w-full object-contain z-10" />
                        <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-20 flex items-center justify-center backdrop-blur-sm">
                          <p className="text-white font-bold tracking-widest uppercase border border-white/20 px-6 py-3 rounded-xl bg-white/5">Replace Image</p>
                        </div>
                      </>
                    ) : (
                      <div className="flex flex-col items-center text-zinc-500 group-hover:text-rose-400 transition-colors">
                        <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-500">
                          <ImageIcon className="w-8 h-8 opacity-70" />
                        </div>
                        <p className="text-sm font-bold tracking-widest uppercase">Drop Image Here</p>
                      </div>
                    )}
                    <input type="file" accept="image/*" onChange={handleImageUpload} className="absolute inset-0 opacity-0 cursor-pointer z-30" />
                  </div>

                  <div className="grid grid-cols-3 sm:grid-cols-4 gap-3">
                    {[
                      { id: 'figure', label: '手办化' }, { id: 'figure_box', label: '盒装手办' },
                      { id: 'cosplay', label: 'COS化' }, { id: 'cosplay_selfie', label: 'COS自拍' },
                      { id: 'real', label: '真人化' }, { id: 'anime', label: '动漫化' },
                      { id: 'chibi', label: 'Q版化' }, { id: 'sticker', label: '贴纸化' },
                      { id: 'first_person', label: '第一视角' }, { id: 'turnaround', label: '三视图' },
                      { id: 'storyboard', label: '分镜化' }, { id: 'random', label: '随机变异' },
                    ].map((effect) => (
                      <button
                        key={effect.id}
                        onClick={() => setImg2ImgEffect(effect.id)}
                        className={`py-3 rounded-xl text-xs font-bold transition-all border ${img2ImgEffect === effect.id ? "bg-rose-500/20 border-rose-500/50 text-rose-300 shadow-[0_0_20px_rgba(244,63,94,0.15)]" : "bg-black/40 border-white/5 text-zinc-500 hover:text-zinc-300 hover:bg-white/5"}`}
                      >
                        {effect.label}
                      </button>
                    ))}
                  </div>

                  <textarea
                    value={img2ImgInput}
                    onChange={(e) => setImg2ImgInput(e.target.value)}
                    placeholder="额外指令 (Optional)..."
                    className="w-full bg-black/40 border border-white/10 rounded-2xl px-5 py-4 text-sm text-zinc-300 placeholder-zinc-700 focus:border-rose-500/50 outline-none transition-all resize-none h-20"
                  />

                  <button
                    onClick={handleImg2ImgSubmit}
                    disabled={imageLoading}
                    className={`w-full py-5 rounded-2xl text-base md:text-lg font-black tracking-widest uppercase transition-all duration-300 flex items-center justify-center gap-3 relative overflow-hidden group ${imageLoading ? "bg-zinc-800 text-zinc-500 cursor-wait" : "bg-white text-black hover:bg-zinc-200 hover:scale-[0.98] shadow-[0_0_40px_rgba(255,255,255,0.15)]"}`}
                  >
                    {imageLoading ? <RefreshCw className="w-6 h-6 animate-spin" /> : <Sparkles className="w-6 h-6" />}
                    {imageLoading ? "PROCESSING..." : "TRANSFORM IMAGE"}
                  </button>
                </div>
              )}
            </div>
            
            {/* Error Message */}
            {error && (
              <div className="p-5 bg-rose-500/10 border border-rose-500/30 rounded-2xl text-rose-300 text-sm font-mono flex items-center gap-3 animate-in fade-in">
                <ShieldAlert className="w-5 h-5 shrink-0" /> {error}
              </div>
            )}

            {/* Results Section */}
            {(result || generatedImage) && (
              <div className="bg-white/[0.02] border border-white/[0.05] rounded-[2rem] p-6 md:p-8 backdrop-blur-xl shadow-2xl space-y-8 animate-in fade-in slide-in-from-bottom-8 mt-4">
                {result && (
                  <div className="space-y-6">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-xs font-mono text-zinc-500 uppercase tracking-widest">
                        <span className="flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
                          {isImg2ImgMode ? "SYSTEM PROMPT" : "POSITIVE PROMPT"}
                        </span>
                        <div className="flex gap-2">
                          {!isVideoMode && (
                            <button 
                              onClick={() => handleGenerateImage(result.prompt)}
                              disabled={imageLoading}
                              className="flex items-center gap-2 px-4 py-1.5 bg-indigo-500 hover:bg-indigo-400 text-white rounded-lg transition-colors disabled:opacity-50 font-bold"
                            >
                              {imageLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <ImageIcon className="w-3.5 h-3.5" />}
                              RENDER
                            </button>
                          )}
                          <button 
                            onClick={() => copyToClipboard(result.prompt, "prompt")}
                            className="flex items-center gap-2 px-4 py-1.5 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors font-bold"
                          >
                            {copied === "prompt" ? "COPIED" : "COPY"}
                          </button>
                        </div>
                      </div>
                      <textarea
                        value={result.prompt}
                        onChange={(e) => setResult({ ...result, prompt: e.target.value })}
                        className="w-full p-5 bg-black/60 border border-white/5 rounded-2xl font-mono text-sm leading-relaxed text-indigo-100/90 h-48 resize-none focus:outline-none focus:border-indigo-500/50 selection:bg-indigo-500/30"
                      />
                    </div>

                    {!isImg2ImgMode && (
                      <div className="space-y-3">
                        <div className="flex items-center justify-between text-xs font-mono text-zinc-500 uppercase tracking-widest">
                          <span className="flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                            NEGATIVE PROMPT
                          </span>
                          <button 
                            onClick={() => copyToClipboard(result.negative_prompt, "negative")}
                            className="flex items-center gap-2 px-4 py-1.5 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-colors font-bold"
                          >
                            {copied === "negative" ? "COPIED" : "COPY"}
                          </button>
                        </div>
                        <textarea
                          value={result.negative_prompt}
                          onChange={(e) => setResult({ ...result, negative_prompt: e.target.value })}
                          className="w-full p-5 bg-black/60 border border-white/5 rounded-2xl font-mono text-sm leading-relaxed text-rose-100/70 h-32 resize-none focus:outline-none focus:border-rose-500/50 selection:bg-rose-500/30"
                        />
                      </div>
                    )}
                    
                    {!isImg2ImgMode && result.recommended_settings && (
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-6 border-t border-white/5">
                        {Object.entries(result.recommended_settings).map(([key, value]) => (
                          <div key={key} className="bg-black/30 p-4 rounded-xl border border-white/5 flex flex-col items-center justify-center text-center">
                            <span className="text-[10px] text-zinc-600 font-mono uppercase tracking-widest mb-1">{key.replace('_', ' ')}</span>
                            <span className="text-sm font-bold text-zinc-300 truncate w-full" title={String(value)}>{String(value)}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {generatedImage && (
                  <div className="space-y-4 pt-6 border-t border-white/5">
                    <div className="flex items-center justify-between text-xs font-mono text-zinc-500 uppercase tracking-widest">
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                        FINAL RENDER
                      </span>
                      <a href={generatedImage} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-4 py-1.5 bg-white/5 hover:bg-white/10 text-white rounded-lg transition-colors font-bold">
                        OPEN FULL
                      </a>
                    </div>
                    <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-black flex justify-center items-center min-h-[300px]">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={generatedImage} alt="Generated" className="max-w-full h-auto max-h-[800px] object-contain" />
                    </div>
                  </div>
                )}
              </div>
            )}

          </div>
        </div>
      </div>

      {/* Sponsor Modal */}
      {showSponsor && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-md p-4 animate-in fade-in" onClick={() => setShowSponsor(false)}>
          <div className="relative bg-zinc-900 border border-white/10 p-8 rounded-[2rem] shadow-2xl max-w-sm w-full" onClick={e => e.stopPropagation()}>
            <button onClick={() => setShowSponsor(false)} className="absolute top-4 right-4 text-zinc-500 hover:text-white transition-colors">
              <X className="w-6 h-6" />
            </button>
            <div className="text-center mb-6">
              <Heart className="w-8 h-8 text-rose-500 mx-auto mb-3" />
              <h3 className="text-2xl font-black text-white tracking-wide">SUPPORT US</h3>
              <p className="text-sm text-zinc-400 mt-2 font-light">您的支持是持续迭代的动力</p>
            </div>
            <div className="bg-white p-3 rounded-2xl">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/zanzhu.png" alt="Sponsor QR" className="w-full h-auto rounded-xl" />
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
"""

    new_content = top_logic + new_ui
    with open('app/page.tsx', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    redesign_ui()
