/* ========== 工具 ========== */
const API = path => `http://127.0.0.1:8080/api/resume/${path}`;
let currentMarkdown = '';   // 当前左侧 Markdown
let currentUserId   = '';   // 当前 ID

/* 生成随机 ID */
function generateID(){
  document.getElementById('userId').value = Math.random().toString(36).slice(2,11);
}

/* 动态增删板块 */
function addEdu(){
  const container = document.getElementById('eduList');
  const idx = container.children.length + 1;
  const div = document.createElement('div');
  div.innerHTML = `
    <input placeholder="学校*" />
    <input placeholder="学位*" />
    <input placeholder="专业*" />
    <input type="month" />-<input type="month" />
    <input placeholder="GPA（可选）" />
    <textarea placeholder="描述（可选）"></textarea>
    <button type="button" onclick="this.parentElement.remove()">删除</button>
  `;
  div.dataset.idx = idx;
  container.appendChild(div);
}
function addExp(){
  const container = document.getElementById('expList');
  const idx = container.children.length + 1;
  const div = document.createElement('div');
  div.innerHTML = `
    <input placeholder="公司*" />
    <input placeholder="职位*" />
    <input type="month" />-<input type="month" />
    <label><input type="checkbox"> 当前工作</label>
    <textarea placeholder="描述（可选）"></textarea>
    <button type="button" onclick="this.parentElement.remove()">删除</button>
  `;
  div.dataset.idx = idx;
  container.appendChild(div);
}
function addSkill(){
  const container = document.getElementById('skillList');
  const idx = container.children.length + 1;
  const div = document.createElement('div');
  div.innerHTML = `
    <input placeholder="技能名称*" />
    <input placeholder="熟练程度（初级/中级/高级）" />
    <input placeholder="类别（如编程语言）" />
    <button type="button" onclick="this.parentElement.remove()">删除</button>
  `;
  div.dataset.idx = idx;
  container.appendChild(div);
}
function addProj(){
  const container = document.getElementById('projList');
  const idx = container.children.length + 1;
  const div = document.createElement('div');
  div.innerHTML = `
    <input placeholder="项目名称*" />
    <input placeholder="项目链接（可选）" />
    <input type="month" />-<input type="month" />
    <textarea placeholder="描述（可选）"></textarea>
    <input placeholder="技术栈（用;分隔）" />
    <button type="button" onclick="this.parentElement.remove()">删除</button>
  `;
  div.dataset.idx = idx;
  container.appendChild(div);
}

/* 初次提交 → 生成左侧预览 */
async function submitInit(){
  const uid = document.getElementById('userId').value.trim();
  if(!uid){ alert('请填写用户ID'); return; }
  currentUserId = uid;
  document.getElementById('saveUserId').value = uid;

  const basic_info = {
    id: uid,
    name: document.getElementById('baseName').value.trim(),
    email: document.getElementById('baseEmail').value.trim(),
    phone: document.getElementById('basePhone').value.trim(),
    address: document.getElementById('baseAddress').value.trim(),
    linkedin: document.getElementById('baseLinkedin').value.trim(),
    github: document.getElementById('baseGithub').value.trim()
  };
  const educations = [], experiences = [], skills = [], projects = [];

  /* 教育 */
  document.querySelectorAll('#eduList>div').forEach((block, i)=>{
    const inp = block.querySelectorAll('input');
    const txa = block.querySelector('textarea');
    educations.push({
      id: i+1,
      school: inp[0].value.trim(),
      degree: inp[1].value.trim(),
      major: inp[2].value.trim(),
      start_date: inp[3].value,
      end_date: inp[4].value,
      gpa: inp[5].value.trim(),
      description: txa.value.trim()
    });
  });
  /* 工作 */
  document.querySelectorAll('#expList>div').forEach((block, i)=>{
    const inp = block.querySelectorAll('input');
    const txa = block.querySelector('textarea');
    experiences.push({
      id: i+1,
      company: inp[0].value.trim(),
      position: inp[1].value.trim(),
      start_date: inp[2].value,
      end_date: inp[3].value,
      is_current: inp[4].checked?1:0,
      description: txa.value.trim()
    });
  });
  /* 技能 */
  document.querySelectorAll('#skillList>div').forEach((block, i)=>{
    const inp = block.querySelectorAll('input');
    skills.push({
      id: i+1,
      skill_name: inp[0].value.trim(),
      proficiency: inp[1].value.trim(),
      category: inp[2].value.trim()
    });
  });
  /* 项目 */
  document.querySelectorAll('#projList>div').forEach((block, i)=>{
    const inp = block.querySelectorAll('input');
    const txa = block.querySelector('textarea');
    projects.push({
      id: i+1,
      project_name: inp[0].value.trim(),
      project_url: inp[1].value.trim(),
      start_date: inp[2].value,
      end_date: inp[3].value,
      description: txa.value.trim(),
      technologies: inp[4].value.trim()
    });
  });

  const payload = { basic_info, educations, experiences, skills, projects };
  const content_request = `请根据以下结构化数据生成一份专业 Markdown 简历：\n${JSON.stringify(payload)}`;

  try{
    const r = await fetch(API('generate'),{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ content_request })
    });
    const j = await r.json();
    if(j.success){
      currentMarkdown = j.generated_content;
      currentMarkdown = currentMarkdown.replace(/^```markdown\s*/, '');
      document.getElementById('resumePreview').innerHTML = marked.parse(currentMarkdown);
      document.getElementById('modalOverlay').style.display='none';
      pushChat('系统','已生成初始简历，可在右侧输入修改需求。');
    }else{
      alert('生成失败：'+j.message);
    }
  }catch(e){ alert('网络错误：'+e); }
}

/* 对话历史 */
function pushChat(sender, txt){
  const box = document.getElementById('chatHistory');
  const div = document.createElement('div');
  div.innerHTML = `<b>${sender}:</b> ${txt}`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

/* 修改简历 */
async function reviseResume(){
  const req = document.getElementById('reviseRequest').value.trim();
  if(!req){ alert('请输入修改需求'); return; }
  pushChat('用户',req);
  try{
    const r = await fetch(API('revise'),{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ resume_content: currentMarkdown, revision_request: req })
    });
    const j = await r.json();
    if(j.success){
      currentMarkdown = j.generated_content;
      document.getElementById('resumePreview').innerHTML = marked.parse(currentMarkdown);
      pushChat('AI','已按需求更新左侧预览。');
      document.getElementById('reviseRequest').value='';
    }else{
      pushChat('系统','修改失败：'+j.message);
    }
  }catch(e){ pushChat('系统','网络错误：'+e); }
}

/* 下载 PDF */
async function downloadPDF(){
  try{
    let cleanMarkdown = currentMarkdown.replace(/^markdown\s+/i, '');
    const r = await fetch(API('markdown-to-pdf'),{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ markdown_content: cleanMarkdown })
    });
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resume_${currentUserId||'anonymous'}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  }catch(e){ alert('下载失败：'+e); }
}

/* 保存 / 读取 */
async function saveResume(){
  const uid = document.getElementById('saveUserId').value.trim();
  if(!uid){ alert('请先填写或生成用户ID'); return; }
  /* 仅示范骨架，可按需把完整 payload 传回 */
  const payload = {
    basic_info:{ id:uid, name:'', email:'', phone:'' },
    educations:[], experiences:[], skills:[], projects:[]
  };
  try{
    const r = await fetch(API('save-resume'),{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const j = await r.json();
    alert(j.message||'保存成功');
  }catch(e){ alert('保存失败：'+e); }
}
async function loadResume(){
  const uid = document.getElementById('saveUserId').value.trim();
  if(!uid){ alert('请先填写用户ID'); return; }
  try{
    const r = await fetch(API(`get-resume/${uid}`));
    const j = await r.json();
    if(j.success){
      /* 实际可再调一次 generate 重新渲染，这里仅展示数据 */
      currentMarkdown = JSON.stringify(j.data,null,2);
      document.getElementById('resumePreview').textContent = currentMarkdown;
      currentUserId = uid;
      alert('读取成功');
    }else{
      alert('读取失败：'+j.message);
    }
  }catch(e){ alert('读取失败：'+e); }
}

/* 页面加载时生成随机 ID */
window.onload = ()=> generateID();
