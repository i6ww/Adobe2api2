document.addEventListener("DOMContentLoaded", () => {
  // Tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.target).classList.add("active");
    });
  });

  // Token Management
  const tokenInput = document.getElementById("tokenInput");
  const addBtn = document.getElementById("addBtn");
  const addMsg = document.getElementById("addMsg");
  const refreshBtn = document.getElementById("refreshBtn");
  const tbody = document.querySelector("#tokenTable tbody");

  const STATUS_MAP = {
    "active": "生效中",
    "exhausted": "额度耗尽",
    "error": "请求异常",
    "disabled": "已禁用"
  };

  async function loadTokens() {
    try {
      const res = await fetch("/api/v1/tokens");
      const data = await res.json();
      renderTable(data.tokens || []);
    } catch (err) {
      console.error(err);
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state" style="color: #ffb4bc;">加载失败</td></tr>`;
    }
  }

  function renderTable(tokens) {
    if (!tokens.length) {
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state">当前没有可用的 Token，请在上方添加。</td></tr>`;
      return;
    }

    tbody.innerHTML = "";
    tokens.forEach(t => {
      const tr = document.createElement("tr");

      const statusClass = `status-${t.status.toLowerCase()}`;
      const isStatusActive = t.status === "active";
      const displayStatus = STATUS_MAP[t.status.toLowerCase()] || t.status;
      
      const d = new Date(t.added_at * 1000);
      const dateStr = d.toLocaleString();

      tr.innerHTML = `
        <td style="color: #a8bfd8; font-size: 12px;" title="添加时间: ${dateStr}">${t.id}</td>
        <td class="token-val">${t.value}</td>
        <td><span class="status-badge ${statusClass}">${displayStatus}</span></td>
        <td style="color: ${t.fails > 0 ? '#ffb4bc' : '#a8bfd8'};">${t.fails}</td>
        <td class="action-btns">
          <button class="small" onclick="toggleToken('${t.id}', '${isStatusActive ? 'disabled' : 'active'}')">
            ${isStatusActive ? '禁用' : '启用'}
          </button>
          <button class="danger" onclick="deleteToken('${t.id}')">删除</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  addBtn.addEventListener("click", async () => {
    const val = tokenInput.value.trim();
    if (!val) {
      showMsg(addMsg, "请先输入 Token 内容", true);
      return;
    }

    addBtn.disabled = true;
    try {
      const res = await fetch("/api/v1/tokens", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: val })
      });
      if (res.ok) {
        tokenInput.value = "";
        showMsg(addMsg, "添加成功", false);
        loadTokens();
      } else {
        showMsg(addMsg, "添加失败，请重试", true);
      }
    } catch (err) {
      showMsg(addMsg, err.message, true);
    }
    addBtn.disabled = false;
  });

  refreshBtn.addEventListener("click", loadTokens);

  window.deleteToken = async (id) => {
    if (!confirm("确定要删除这个 Token 吗？")) return;
    try {
      await fetch(`/api/v1/tokens/${id}`, { method: "DELETE" });
      loadTokens();
    } catch (err) {
      alert("删除失败");
    }
  };

  window.toggleToken = async (id, newStatus) => {
    try {
      await fetch(`/api/v1/tokens/${id}/status?status=${newStatus}`, { method: "PUT" });
      loadTokens();
    } catch (err) {
      alert("状态更新失败");
    }
  };

  // Config Management
  const confApiKey = document.getElementById("confApiKey");
  const confUseProxy = document.getElementById("confUseProxy");
  const confProxy = document.getElementById("confProxy");
  const confGenerateTimeout = document.getElementById("confGenerateTimeout");
  const saveConfigBtn = document.getElementById("saveConfigBtn");
  const configMsg = document.getElementById("configMsg");

  // Logs
  const logsTbody = document.querySelector("#logsTable tbody");
  const refreshLogsBtn = document.getElementById("refreshLogsBtn");
  const clearLogsBtn = document.getElementById("clearLogsBtn");

  async function loadConfig() {
    try {
      const res = await fetch("/api/v1/config");
      if (res.ok) {
        const data = await res.json();
        confApiKey.value = data.api_key || "";
        confUseProxy.checked = data.use_proxy || false;
        confProxy.value = data.proxy || "";
        confGenerateTimeout.value = Number(data.generate_timeout || 180);
      }
    } catch (err) {
      console.error("加载配置失败", err);
    }
  }

  saveConfigBtn.addEventListener("click", async () => {
    saveConfigBtn.disabled = true;
    try {
      // 保留未在此页面显示的配置项
      const currentRes = await fetch("/api/v1/config");
      const currentData = await currentRes.json();
      
      const payload = {
        ...currentData,
        api_key: confApiKey.value.trim(),
        use_proxy: confUseProxy.checked,
        proxy: confProxy.value.trim(),
        generate_timeout: Math.max(30, Math.min(600, Number(confGenerateTimeout.value || 180))),
      };

      const res = await fetch("/api/v1/config", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showMsg(configMsg, "配置已保存", false);
      } else {
        showMsg(configMsg, "保存失败，请检查服务状态", true);
      }
    } catch (err) {
      showMsg(configMsg, err.message, true);
    }
    saveConfigBtn.disabled = false;
  });

  async function loadLogs() {
    if (!logsTbody) return;
    try {
      const res = await fetch("/api/v1/logs?limit=200");
      if (!res.ok) throw new Error("加载日志失败");
      const data = await res.json();
      renderLogs(data.logs || []);
    } catch (err) {
      logsTbody.innerHTML = `<tr><td colspan="7" class="empty-state" style="color: #ffb4bc;">${err.message || "日志加载失败"}</td></tr>`;
    }
  }

  function renderLogs(logs) {
    if (!logs.length) {
      logsTbody.innerHTML = `<tr><td colspan="7" class="empty-state">暂无请求日志</td></tr>`;
      return;
    }

    logsTbody.innerHTML = "";
    logs.forEach(item => {
      const tr = document.createElement("tr");
      const dt = new Date((item.ts || 0) * 1000);
      const t = Number(item.duration_sec || 0);
      const status = Number(item.status_code || 0);
      const statusClass = status >= 500 ? "log-status-5xx" : (status >= 400 ? "log-status-4xx" : "log-status-2xx");
      tr.innerHTML = `
        <td style="white-space: nowrap; color: #a8bfd8;">${dt.toLocaleString()}</td>
        <td><code>${item.operation || "-"}</code> <span style="color:#a8bfd8;">${item.path || "-"}</span></td>
        <td><span class="status-badge ${statusClass}">${status || "-"}</span></td>
        <td style="color:${t > 30 ? "#ffb4bc" : "#a8bfd8"};">${t}</td>
        <td class="token-val">${item.model || "-"}</td>
        <td title="${(item.prompt_preview || "").replace(/"/g, "&quot;")}" style="max-width: 280px; color: #a8bfd8;">${item.prompt_preview || "-"}</td>
        <td style="font-family: 'IBM Plex Mono', monospace; color:#a8bfd8;">${item.client_ip || "-"}</td>
      `;
      logsTbody.appendChild(tr);
    });
  }

  if (refreshLogsBtn) {
    refreshLogsBtn.addEventListener("click", loadLogs);
  }

  if (clearLogsBtn) {
    clearLogsBtn.addEventListener("click", async () => {
      if (!confirm("确定清空请求日志吗？")) return;
      try {
        const res = await fetch("/api/v1/logs", { method: "DELETE" });
        if (!res.ok) throw new Error("清空失败");
        loadLogs();
      } catch (err) {
        alert(err.message || "清空失败");
      }
    });
  }


  function showMsg(el, text, isError) {
    el.textContent = text;
    el.style.color = isError ? "#ffb4bc" : "#4de2c4";
    setTimeout(() => { el.textContent = ""; }, 3000);
  }

  // Init
  loadTokens();
  loadConfig();
  loadLogs();
});
