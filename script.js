// ====== 表单提交处理 ======
// 当前使用 Formspree 免费版作为后端
// 替换下面的 FORM_ENDPOINT 为你自己的 Formspree 表单ID 或自建后端地址

const FORM_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';

document.getElementById('consult-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const form = e.target;
  const resultDiv = document.getElementById('form-result');
  const submitBtn = form.querySelector('.btn-submit');

  // 收集表单数据
  const formData = {
    name: form.name.value.trim(),
    phone: form.phone.value.trim(),
    idcard: form.idcard.value.trim() || '(未填写)',
    school: form.school.value.trim(),
    message: form.message.value.trim() || '(未填写)',
    submittedAt: new Date().toLocaleString('zh-CN')
  };

  // 手机号格式二次校验
  if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
    showResult('请输入正确的11位手机号', 'error');
    return;
  }

  // 身份证号必填校验
  if (!formData.idcard || formData.idcard === '(未填写)') {
    showResult('请填写身份证号（用于招生资格审核）', 'error');
    return;
  }
  if (!/^\d{17}[\dXx]$/.test(formData.idcard)) {
    showResult('身份证号格式不正确，请检查（18位）', 'error');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = '提交中...';

  try {
    const response = await fetch(FORM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      showResult('✅ 提交成功！学长会在24小时内联系你，请保持手机畅通~', 'success');
      form.reset();
    } else {
      const errData = await response.json().catch(() => ({}));
      showResult('提交失败：' + (errData.error || '网络错误，请稍后再试'), 'error');
    }
  } catch (err) {
    showResult('网络连接失败，请检查网络后重试', 'error');
  }

  submitBtn.disabled = false;
  submitBtn.textContent = '提交咨询申请';
});

function showResult(msg, type) {
  const resultDiv = document.getElementById('form-result');
  resultDiv.textContent = msg;
  resultDiv.className = 'form-result ' + type;
  resultDiv.style.display = 'block';
}

// ====== 导航栏滚动阴影 ======
window.addEventListener('scroll', function() {
  const navbar = document.getElementById('navbar');
  if (window.scrollY > 10) {
    navbar.style.boxShadow = '0 2px 12px rgba(0,0,0,0.08)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});
