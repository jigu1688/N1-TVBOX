const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const autoInstallCheck = document.getElementById('autoInstallCheck');
const progressBox = document.getElementById('progressBox');
const progressFill = document.getElementById('progressFill');
const progressPct = document.getElementById('progress-pct');
const progressName = document.getElementById('progress-name');
const fileList = document.getElementById('fileList');
const storageText = document.getElementById('storage-text');
const storageFill = document.getElementById('storageFill');
const uploadStatus = document.getElementById('upload-status');

if (dropZone && fileInput) {
    dropZone.onclick = () => fileInput.click();
    dropZone.ondragover = e => { e.preventDefault(); dropZone.classList.add('dragover'); };
    dropZone.ondragleave = () => dropZone.classList.remove('dragover');
    dropZone.ondrop = e => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
      if (e.dataTransfer && e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
    };
    fileInput.onchange = () => { if (fileInput.files.length) uploadFiles(fileInput.files); };
}

async function loadStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    if (storageText) storageText.innerText = `${data.storageFree} 可用 / ${data.storageTotal} 总计`;
    if (storageFill) storageFill.style.width = `${data.storagePercent}%`;
    renderFiles(data.files);
  } catch (e) {}
}

function renderFiles(files) {
  if (!fileList) return;
  if (!files || files.length === 0) {
    fileList.innerHTML = '<div style="color:var(--text-dim); text-align:center; padding:20px;">暂无已接收文件</div>';
    return;
  }
  fileList.innerHTML = files.map(f => `
    <div class="file-item">
      <div class="file-info">
        <div class="file-name">${f.name}</div>
        <div class="file-meta">${f.size} · ${f.date}</div>
      </div>
      <div class="btn-group">
        ${f.isApk ? `<button class="btn btn-install" onclick="installApk('${f.name}')">一键安装</button>` : ''}
        <button class="btn btn-del" onclick="deleteFile('${f.name}')">删除</button>
      </div>
    </div>
  `).join('');
}

async function uploadFiles(files) {
  for (let i = 0; i < files.length; i++) {
    await uploadSingle(files[i]);
  }
  loadStatus();
}

function uploadSingle(file) {
  return new Promise((resolve) => {
    if (progressBox) progressBox.style.display = 'block';
    if (progressName) progressName.innerText = `正在上传: ${file.name}`;
    if (uploadStatus) uploadStatus.innerText = '传输中...';
    const xhr = new XMLHttpRequest();
    const fd = new FormData();
    fd.append('file', file);
    xhr.upload.onprogress = e => {
      if (e.lengthComputable) {
        const pct = Math.round((e.loaded / e.total) * 100);
        if (progressFill) progressFill.style.width = pct + '%';
        if (progressPct) progressPct.innerText = pct + '%';
      }
    };
    xhr.onload = () => {
      if (progressBox) progressBox.style.display = 'none';
      if (uploadStatus) {
        uploadStatus.innerText = '上传成功！';
        setTimeout(() => uploadStatus.innerText = '就绪', 3000);
      }
      resolve();
    };
    xhr.onerror = () => { 
      if (uploadStatus) uploadStatus.innerText = '上传失败'; 
      resolve(); 
    };
    xhr.open('POST', '/api/upload');
    if (autoInstallCheck && autoInstallCheck.checked) xhr.setRequestHeader('X-Auto-Install', '1');
    xhr.send(fd);
  });
}

async function installApk(name) {
  if (uploadStatus) uploadStatus.innerText = `正在安装 ${name}...`;
  try {
    const res = await fetch('/api/install', { method: 'POST', body: JSON.stringify({ fileName: name }) });
    const data = await res.json();
    if (uploadStatus) uploadStatus.innerText = data.status === 'ok' ? '安装成功！' : '已弹出安装向导';
  } catch (e) {
    if (uploadStatus) uploadStatus.innerText = '安装已触发';
  }
  setTimeout(() => { if (uploadStatus) uploadStatus.innerText = '就绪'; }, 3000);
}

async function deleteFile(name) {
  if (!confirm(`确定删除 ${name} 吗？`)) return;
  await fetch('/api/delete', { method: 'POST', body: JSON.stringify({ fileName: name }) });
  loadStatus();
}

loadStatus();
setInterval(loadStatus, 5000);
