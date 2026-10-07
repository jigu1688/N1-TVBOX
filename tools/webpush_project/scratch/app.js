// NextGen 隔空传装 & 文件管理器 Web 控制台
(function() {
  'use strict';

  // DOM Elements - Tabs
  const tabPush = document.getElementById('tab-push');
  const tabFs = document.getElementById('tab-fs');
  const viewPush = document.getElementById('view-push');
  const viewFs = document.getElementById('view-fs');

  // Push Tab Elements
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

  // FS Tab Elements
  const fsBreadcrumb = document.getElementById('fs-breadcrumb');
  const fsStorageChips = document.getElementById('fs-storage-chips');
  const fsStorageText = document.getElementById('fs-storage-text');
  const fsStorageFill = document.getElementById('fs-storage-fill');
  const fsTableBody = document.getElementById('fs-table-body');
  const fsSearchInput = document.getElementById('fs-search-input');
  const fsUploadInput = document.getElementById('fs-upload-input');
  const fsDropZone = document.getElementById('fs-drop-zone');

  // Modal Elements
  const modalOverlay = document.getElementById('modalOverlay');
  const modalTitle = document.getElementById('modalTitle');
  const modalInput = document.getElementById('modalInput');
  const modalBtnConfirm = document.getElementById('modalBtnConfirm');
  const modalBtnCancel = document.getElementById('modalBtnCancel');

  // Toast Container
  const toastContainer = document.getElementById('toastContainer');

  // State
  let currentPath = '/sdcard';
  let parentPath = '';
  let fsItems = [];
  let modalCallback = null;

  // Tab switching
  function switchTab(tab) {
    if (tab === 'push') {
      tabPush.classList.add('active');
      tabFs.classList.remove('active');
      viewPush.style.display = 'flex';
      viewFs.style.display = 'none';
      loadStatus();
    } else {
      tabFs.classList.add('active');
      tabPush.classList.remove('active');
      viewFs.style.display = 'flex';
      viewPush.style.display = 'none';
      loadFs(currentPath);
    }
  }

  if (tabPush && tabFs) {
    tabPush.onclick = () => switchTab('push');
    tabFs.onclick = () => switchTab('fs');
  }

  // Toast Notification
  function showToast(msg, type = 'info') {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = msg;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // Modal helper
  function openModal(title, defaultValue, onConfirm) {
    if (!modalOverlay || !modalInput || !modalTitle) return;
    modalTitle.innerText = title;
    modalInput.value = defaultValue || '';
    modalOverlay.style.display = 'flex';
    modalInput.focus();
    modalCallback = onConfirm;
  }

  function closeModal() {
    if (!modalOverlay) return;
    modalOverlay.style.display = 'none';
    modalCallback = null;
  }

  if (modalBtnCancel) modalBtnCancel.onclick = closeModal;
  if (modalBtnConfirm) {
    modalBtnConfirm.onclick = () => {
      if (modalCallback) {
        const val = modalInput.value.trim();
        modalCallback(val);
      }
      closeModal();
    };
  }
  if (modalInput) {
    modalInput.onkeydown = (e) => {
      if (e.key === 'Enter') {
        if (modalCallback) {
          modalCallback(modalInput.value.trim());
        }
        closeModal();
      } else if (e.key === 'Escape') {
        closeModal();
      }
    };
  }

  // --- Push Tab Logic ---
  if (dropZone && fileInput) {
    dropZone.onclick = () => fileInput.click();
    dropZone.ondragover = e => { e.preventDefault(); dropZone.classList.add('dragover'); };
    dropZone.ondragleave = () => dropZone.classList.remove('dragover');
    dropZone.ondrop = e => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
      if (e.dataTransfer && e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files, null, true);
    };
    fileInput.onchange = () => {
      if (fileInput.files.length) uploadFiles(fileInput.files, null, true);
    };
  }

  async function loadStatus() {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      if (storageText) storageText.innerText = `${data.storageFree} 可用 / ${data.storageTotal} 总计`;
      if (storageFill) storageFill.style.width = `${data.storagePercent}%`;
      renderPushFiles(data.files);
    } catch (e) {}
  }

  function renderPushFiles(files) {
    if (!fileList) return;
    if (!files || files.length === 0) {
      fileList.innerHTML = '<div style="color:var(--text-dim); text-align:center; padding:24px;">暂无已接收文件</div>';
      return;
    }
    fileList.innerHTML = files.map(f => `
      <div class="file-item">
        <div class="file-info">
          <div class="file-name">${escapeHtml(f.name)}</div>
          <div class="file-meta">${f.size} · ${f.date}</div>
        </div>
        <div class="btn-group">
          ${f.isApk ? `<button class="btn btn-install" onclick="window.NextGen.installApk('${escapeJs(f.name)}')">一键安装</button>` : ''}
          <a class="btn btn-down" href="/download/${encodeURIComponent(f.name)}" download="${escapeHtml(f.name)}">下载</a>
          <button class="btn btn-del" onclick="window.NextGen.deletePushFile('${escapeJs(f.name)}')">删除</button>
        </div>
      </div>
    `).join('');
  }

  // --- File Manager (FS) Logic ---
  async function loadFs(path) {
    try {
      const target = path || currentPath || '/sdcard';
      const res = await fetch(`/api/fs/list?path=${encodeURIComponent(target)}`);
      const data = await res.json();

      currentPath = data.currentPath;
      parentPath = data.parentPath;
      fsItems = data.items || [];

      // Render Storages
      renderFsStorages(data.storages || []);

      // Render Breadcrumb
      renderFsBreadcrumb(data.currentPath);

      // Render Capacity
      if (fsStorageText) fsStorageText.innerText = `${data.storageFree} 可用 / ${data.storageTotal} 总计 (${data.storagePercent}% 已用)`;
      if (fsStorageFill) fsStorageFill.style.width = `${data.storagePercent}%`;

      // Render Table
      filterAndRenderFsTable();
    } catch (e) {
      showToast('加载目录失败: ' + e.message, 'error');
    }
  }

  function renderFsStorages(storages) {
    if (!fsStorageChips) return;
    fsStorageChips.innerHTML = storages.map(s => {
      const activeClass = currentPath.startsWith(s.path) ? 'storage-chip-active' : '';
      let icon = '📱';
      if (s.name.includes('U盘') || s.name.includes('外接') || s.path.includes('/storage/')) icon = '💾';
      else if (s.name.includes('下载')) icon = '📥';
      else if (s.name.includes('影视')) icon = '🎬';
      return `<button class="storage-chip ${activeClass}" onclick="window.NextGen.navigateTo('${escapeJs(s.path)}')">${icon} ${escapeHtml(s.name)}</button>`;
    }).join('');
  }

  function renderFsBreadcrumb(path) {
    if (!fsBreadcrumb) return;
    const parts = path.split('/').filter(Boolean);
    let accumulated = '';
    let html = `<span class="bc-item" onclick="window.NextGen.navigateTo('/')">根目录</span>`;
    for (let i = 0; i < parts.length; i++) {
      accumulated += '/' + parts[i];
      const p = accumulated;
      html += `<span class="bc-sep">/</span><span class="bc-item" onclick="window.NextGen.navigateTo('${escapeJs(p)}')">${escapeHtml(parts[i])}</span>`;
    }
    fsBreadcrumb.innerHTML = html;
  }

  function filterAndRenderFsTable() {
    if (!fsTableBody) return;
    const query = fsSearchInput ? fsSearchInput.value.trim().toLowerCase() : '';
    const filtered = query ? fsItems.filter(item => item.name.toLowerCase().includes(query)) : fsItems;

    if (filtered.length === 0) {
      fsTableBody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:32px; color:var(--text-dim);">当前目录为空或无匹配项</td></tr>`;
      return;
    }

    fsTableBody.innerHTML = filtered.map(item => {
      const icon = getFileIcon(item.type, item.isDir);
      const nameClick = item.isDir 
        ? `onclick="window.NextGen.navigateTo('${escapeJs(item.path)}')"` 
        : '';
      const nameStyle = item.isDir ? 'cursor:pointer; font-weight:600; color:#38bdf8;' : '';

      return `
        <tr class="fs-row">
          <td class="fs-td-name" ${nameClick} style="${nameStyle}">
            <span class="fs-icon">${icon}</span>
            <span class="fs-name-text" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</span>
          </td>
          <td class="fs-td-size">${item.size}</td>
          <td class="fs-td-date">${item.date}</td>
          <td class="fs-td-actions">
            ${item.isApk ? `<button class="btn btn-sm btn-install" onclick="window.NextGen.installFsApk('${escapeJs(item.path)}')">安装</button>` : ''}
            ${!item.isDir ? `<a class="btn btn-sm btn-down" href="/api/fs/download?path=${encodeURIComponent(item.path)}" download="${escapeHtml(item.name)}">下载</a>` : ''}
            <button class="btn btn-sm btn-edit" onclick="window.NextGen.renameFsItem('${escapeJs(item.path)}', '${escapeJs(item.name)}')">重命名</button>
            <button class="btn btn-sm btn-del" onclick="window.NextGen.deleteFsItem('${escapeJs(item.path)}', '${escapeJs(item.name)}', ${item.isDir})">删除</button>
          </td>
        </tr>
      `;
    }).join('');
  }

  function getFileIcon(type, isDir) {
    if (isDir) return '📁';
    switch (type) {
      case 'apk': return '📦';
      case 'video': return '🎬';
      case 'audio': return '🎵';
      case 'image': return '🖼️';
      case 'archive': return '🗜️';
      case 'text': return '📄';
      default: return '📄';
    }
  }

  if (fsSearchInput) {
    fsSearchInput.oninput = () => filterAndRenderFsTable();
  }

  // FS Drag and drop upload
  if (fsDropZone && fsUploadInput) {
    fsDropZone.ondragover = e => { e.preventDefault(); fsDropZone.classList.add('dragover'); };
    fsDropZone.ondragleave = () => fsDropZone.classList.remove('dragover');
    fsDropZone.ondrop = e => {
      e.preventDefault();
      fsDropZone.classList.remove('dragover');
      if (e.dataTransfer && e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files, currentPath, false);
    };
    fsUploadInput.onchange = () => {
      if (fsUploadInput.files.length) uploadFiles(fsUploadInput.files, currentPath, false);
    };
  }

  // Upload Engine
  async function uploadFiles(files, targetDir, isPushTab) {
    for (let i = 0; i < files.length; i++) {
      await uploadSingle(files[i], targetDir, isPushTab);
    }
    if (isPushTab) {
      loadStatus();
    } else {
      loadFs(currentPath);
    }
  }

  function uploadSingle(file, targetDir, isPushTab) {
    return new Promise((resolve) => {
      if (progressBox) progressBox.style.display = 'block';
      if (progressName) progressName.innerText = `正在传输: ${file.name}`;
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
          uploadStatus.innerText = '传输完成！';
          setTimeout(() => uploadStatus.innerText = '就绪', 3000);
        }
        showToast(`文件 ${file.name} 传输成功！`, 'success');
        resolve();
      };

      xhr.onerror = () => {
        if (uploadStatus) uploadStatus.innerText = '传输失败';
        showToast(`文件 ${file.name} 传输失败`, 'error');
        resolve();
      };

      const url = targetDir ? `/api/fs/upload?path=${encodeURIComponent(targetDir)}` : '/api/upload';
      xhr.open('POST', url);
      if (isPushTab && autoInstallCheck && autoInstallCheck.checked) {
        xhr.setRequestHeader('X-Auto-Install', '1');
      }
      xhr.send(fd);
    });
  }

  // Global actions for onclick
  window.NextGen = {
    navigateTo(path) {
      loadFs(path);
    },
    goParent() {
      if (parentPath) loadFs(parentPath);
      else showToast('已经是顶层目录', 'info');
    },
    refresh() {
      loadFs(currentPath);
      showToast('目录已刷新', 'info');
    },
    createFolderPrompt() {
      openModal('新建文件夹', '新建文件夹', async (name) => {
        if (!name) return;
        try {
          const res = await fetch('/api/fs/mkdir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: currentPath, name })
          });
          const data = await res.json();
          if (data.status === 'ok') {
            showToast(`文件夹 "${name}" 创建成功！`, 'success');
            loadFs(currentPath);
          } else {
            showToast('创建失败: ' + (data.error || '未知错误'), 'error');
          }
        } catch (e) {
          showToast('创建异常: ' + e.message, 'error');
        }
      });
    },
    triggerFsUpload() {
      if (fsUploadInput) fsUploadInput.click();
    },
    renameFsItem(path, oldName) {
      openModal(`重命名 "${oldName}"`, oldName, async (newName) => {
        if (!newName || newName === oldName) return;
        try {
          const res = await fetch('/api/fs/rename', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path, newName })
          });
          const data = await res.json();
          if (data.status === 'ok') {
            showToast(`已重命名为 "${newName}"`, 'success');
            loadFs(currentPath);
          } else {
            showToast('重命名失败', 'error');
          }
        } catch (e) {
          showToast('重命名异常: ' + e.message, 'error');
        }
      });
    },
    async deleteFsItem(path, name, isDir) {
      const typeText = isDir ? '文件夹及其所有内容' : '文件';
      if (!confirm(`确定要永久删除 ${typeText} "${name}" 吗？此操作无法撤销！`)) return;
      try {
        const res = await fetch('/api/fs/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path })
        });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast(`已删除 "${name}"`, 'success');
          loadFs(currentPath);
        } else {
          showToast('删除失败', 'error');
        }
      } catch (e) {
        showToast('删除异常: ' + e.message, 'error');
      }
    },
    async installFsApk(path) {
      showToast('正在静默安装 APK，请稍候...', 'info');
      try {
        const res = await fetch('/api/fs/install', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path })
        });
        const data = await res.json();
        if (data.status === 'ok') {
          showToast('APK 静默安装成功！已可在桌面打开', 'success');
        } else {
          showToast('已下发系统安装请求，请在电视画面确认', 'info');
        }
      } catch (e) {
        showToast('安装触发异常: ' + e.message, 'error');
      }
    },
    async installApk(name) {
      if (uploadStatus) uploadStatus.innerText = `正在安装 ${name}...`;
      showToast(`正在安装 ${name}...`, 'info');
      try {
        const res = await fetch('/api/install', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ fileName: name })
        });
        const data = await res.json();
        const msg = data.status === 'ok' ? '安装成功！' : '已弹出安装向导';
        if (uploadStatus) uploadStatus.innerText = msg;
        showToast(msg, 'success');
      } catch (e) {
        showToast('安装已触发', 'info');
      }
      setTimeout(() => { if (uploadStatus) uploadStatus.innerText = '就绪'; }, 3000);
    },
    async deletePushFile(name) {
      if (!confirm(`确定删除 ${name} 吗？`)) return;
      await fetch('/api/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileName: name })
      });
      showToast(`已删除 ${name}`, 'success');
      loadStatus();
    }
  };

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeJs(str) {
    if (!str) return '';
    return String(str).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
  }

  // Initial loads
  loadStatus();
  setInterval(() => {
    if (tabPush && tabPush.classList.contains('active')) {
      loadStatus();
    }
  }, 6000);

})();
