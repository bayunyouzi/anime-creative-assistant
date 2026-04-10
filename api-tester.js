const http = require('http');

const HTML = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API 本地连通性测试工具</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen p-6">
    <div class="max-w-5xl mx-auto space-y-6">
        <div class="text-center space-y-2">
            <h1 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-rose-400">
                API 连通性测试工具
            </h1>
            <p class="text-gray-400 text-sm">用于测试接口是否被拦截、模型是否支持。请求由本地 Node.js 发出，绕过浏览器 CORS 限制。</p>
        </div>

        <div class="grid md:grid-cols-2 gap-6">
            <!-- 配置面板 -->
            <div class="bg-gray-800 border border-gray-700 p-6 rounded-2xl space-y-4 shadow-xl">
                <h2 class="text-xl font-bold flex items-center gap-2 border-b border-gray-700 pb-3">
                    ⚙️ 接口配置
                </h2>
                
                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">测试类型</label>
                    <select id="apiType" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none transition">
                        <option value="chat">💬 文本生成 (Chat Completions)</option>
                        <option value="image">🎨 图像生成 (Image Generations)</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">接口地址 (Endpoint)</label>
                    <input id="endpoint" type="text" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none" 
                           value="https://apifree.rensumo.top/v1/chat/completions">
                </div>

                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">API Key</label>
                    <input id="apiKey" type="text" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none" 
                           value="sk-4SY28cVkJZKAckHGavYlJGyF9SfuFCs7dpbJGbBYEREtG8Oe">
                </div>

                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">模型名称 (Model)</label>
                    <input id="model" type="text" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none" 
                           value="openai/gpt-oss-20b">
                </div>

                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">User-Agent (浏览器伪装头)</label>
                    <textarea id="userAgent" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none text-xs" rows="2">Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36</textarea>
                </div>

                <div>
                    <label class="block text-xs font-bold text-gray-400 mb-1">测试提示词 (Prompt)</label>
                    <textarea id="prompt" class="w-full bg-gray-900 border border-gray-700 p-2.5 rounded-lg focus:border-indigo-500 outline-none h-20">你好，请测试一下连通性，回复“连接成功”。</textarea>
                </div>

                <button onclick="sendRequest()" id="sendBtn" class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 py-3 rounded-xl font-bold text-white shadow-lg transition-all active:scale-95">
                    🚀 发送测试请求
                </button>
            </div>

            <!-- 结果面板 -->
            <div class="bg-gray-800 border border-gray-700 p-6 rounded-2xl flex flex-col shadow-xl">
                <h2 class="text-xl font-bold flex items-center gap-2 border-b border-gray-700 pb-3 mb-4">
                    📡 响应结果
                </h2>
                
                <div id="loading" class="hidden flex items-center justify-center py-10 text-indigo-400 font-bold animate-pulse">
                    ⏳ 请求中，请稍候...
                </div>
                
                <div id="resultContainer" class="flex-1 flex flex-col">
                    <div class="flex gap-4 mb-2 text-xs font-mono">
                        <span id="statusBadge" class="hidden px-2 py-1 rounded bg-gray-700"></span>
                        <span id="timeBadge" class="hidden px-2 py-1 rounded bg-gray-700"></span>
                    </div>
                    
                    <pre id="result" class="flex-1 bg-gray-900 border border-gray-700 p-4 rounded-xl overflow-auto text-xs font-mono text-gray-300 whitespace-pre-wrap min-h-[200px] max-h-[500px]"></pre>
                    
                    <div id="imgPreview" class="hidden mt-4 bg-gray-900 border border-gray-700 p-2 rounded-xl flex justify-center items-center">
                        <img id="resultImg" class="max-w-full rounded-lg" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('apiType').addEventListener('change', (e) => {
            const endpointInput = document.getElementById('endpoint');
            const modelInput = document.getElementById('model');
            const promptInput = document.getElementById('prompt');
            
            if (e.target.value === 'image') {
                if(endpointInput.value.includes('chat/completions')) endpointInput.value = 'https://api.example.com/v1/images/generations';
                if(modelInput.value === 'openai/gpt-oss-20b') modelInput.value = 'dall-e-3';
                promptInput.value = 'A beautiful anime girl, masterpiece, best quality';
            } else {
                if(endpointInput.value.includes('images/generations')) endpointInput.value = 'https://apifree.rensumo.top/v1/chat/completions';
                if(modelInput.value === 'dall-e-3') modelInput.value = 'openai/gpt-oss-20b';
                promptInput.value = '你好，请测试一下连通性，回复“连接成功”。';
            }
        });

        async function sendRequest() {
            const btn = document.getElementById('sendBtn');
            const loading = document.getElementById('loading');
            const resultBox = document.getElementById('result');
            const imgPreview = document.getElementById('imgPreview');
            const resultImg = document.getElementById('resultImg');
            const statusBadge = document.getElementById('statusBadge');
            const timeBadge = document.getElementById('timeBadge');

            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            loading.classList.remove('hidden');
            resultBox.textContent = '';
            imgPreview.classList.add('hidden');
            statusBadge.classList.add('hidden');
            timeBadge.classList.add('hidden');

            const payload = {
                type: document.getElementById('apiType').value,
                endpoint: document.getElementById('endpoint').value,
                apiKey: document.getElementById('apiKey').value,
                model: document.getElementById('model').value,
                userAgent: document.getElementById('userAgent').value,
                prompt: document.getElementById('prompt').value
            };

            try {
                const res = await fetch('/api/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await res.json();
                
                // 渲染状态徽章
                statusBadge.textContent = "HTTP " + data.status + " " + data.statusText;
                statusBadge.classList.remove('hidden', 'bg-gray-700', 'bg-green-900', 'text-green-400', 'bg-red-900', 'text-red-400');
                if (data.status === 200) {
                    statusBadge.classList.add('bg-green-900', 'text-green-400');
                } else {
                    statusBadge.classList.add('bg-red-900', 'text-red-400');
                }

                timeBadge.textContent = "耗时 " + data.durationMs + "ms";
                timeBadge.classList.remove('hidden');

                // 渲染结果
                resultBox.textContent = JSON.stringify(data.data, null, 2);

                // 尝试渲染图片
                let imageUrl = null;
                if (data.status === 200 && payload.type === 'image') {
                    const resData = data.data;
                    // 1. 尝试从标准 DALL-E 格式提取
                    if (resData?.data?.[0]?.url) {
                        imageUrl = resData.data[0].url;
                    } else if (resData?.choices?.[0]?.message?.content) {
                        const content = resData.choices[0].message.content;
                        if (typeof content === 'string') {
                            const httpPos = Math.max(content.indexOf('https://'), content.indexOf('http://'));
                            if (httpPos >= 0) {
                                let end = content.length;
                                const spacePos = content.indexOf(' ', httpPos);
                                const linePos = content.indexOf('\\n', httpPos);
                                const closePos = content.indexOf(')', httpPos);
                                if (spacePos >= 0 && spacePos < end) end = spacePos;
                                if (linePos >= 0 && linePos < end) end = linePos;
                                if (closePos >= 0 && closePos < end) end = closePos;
                                imageUrl = content.slice(httpPos, end).trim();
                            }
                        }
                    }
                }

                if (imageUrl) {
                    resultImg.src = imageUrl;
                    imgPreview.classList.remove('hidden');
                }
            } catch (e) {
                statusBadge.textContent = '本地错误';
                statusBadge.classList.remove('hidden', 'bg-gray-700');
                statusBadge.classList.add('bg-red-900', 'text-red-400');
                
                resultBox.textContent = e.message;
            } finally {
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
                loading.classList.add('hidden');
            }
        }
    </script>
</body>
</html>
`;

const server = http.createServer(async (req, res) => {
    // 根路由，返回 UI 界面
    if (req.url === '/' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(HTML);
        return;
    }

    // 测试接口路由
    if (req.url === '/api/test' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', async () => {
            try {
                const { type, endpoint, apiKey, model, userAgent, prompt } = JSON.parse(body);
                
                const headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + apiKey,
                    'User-Agent': userAgent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                };

                let apiPayload;
                // If the endpoint is chat/completions but we are doing image generation (like grok-imagine-1.0),
                // we need to use the chat messages format, not the DALL-E format.
                if (type === 'chat' || endpoint.includes('chat/completions')) {
                    apiPayload = { model, messages: [{ role: 'user', content: prompt }] };
                } else {
                    apiPayload = { model, prompt, n: 1 };
                }

                const startTime = Date.now();
                
                // 使用 Node.js 内置的 fetch (Node 18+)
                const apiRes = await fetch(endpoint, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify(apiPayload)
                });
                
                const duration = Date.now() - startTime;
                const contentType = apiRes.headers.get('content-type') || '';
                
                let responseData;
                if (contentType.includes('application/json')) {
                    responseData = await apiRes.json();
                } else {
                    responseData = await apiRes.text();
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    status: apiRes.status,
                    statusText: apiRes.statusText,
                    durationMs: duration,
                    data: responseData
                }));
            } catch (e) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ 
                    status: 500,
                    statusText: "Internal Error",
                    durationMs: 0,
                    data: { error: "本地代理请求失败: " + e.message } 
                }));
            }
        });
        return;
    }

    res.writeHead(404);
    res.end('Not found');
});

const START_PORT = Number(process.env.PORT) || 8888;
let currentPort = START_PORT;
let remainingRetries = 10;

const printStarted = () => {
    console.log('\x1b[32m%s\x1b[0m', '✅ API 本地测试工具已启动！');
    console.log('\x1b[36m%s\x1b[0m', '👉 请在浏览器中打开: http://localhost:' + currentPort);
    console.log('\x1b[90m%s\x1b[0m', '   (按 Ctrl+C 关闭)');
};

server.on('listening', printStarted);
server.on('error', (err) => {
    if (err && err.code === 'EADDRINUSE' && remainingRetries > 0) {
        const nextPort = currentPort + 1;
        console.log('\x1b[33m%s\x1b[0m', `⚠️ 端口 ${currentPort} 被占用，自动切换到 ${nextPort}...`);
        currentPort = nextPort;
        remainingRetries -= 1;
        setTimeout(() => server.listen(currentPort), 50);
        return;
    }
    if (err && err.code === 'EADDRINUSE') {
        console.error('\x1b[31m%s\x1b[0m', `❌ 端口 ${START_PORT} 起连续多个端口均被占用，请关闭占用进程或设置 PORT 环境变量。`);
        process.exit(1);
    }
    console.error(err);
    process.exit(1);
});

server.listen(currentPort);
