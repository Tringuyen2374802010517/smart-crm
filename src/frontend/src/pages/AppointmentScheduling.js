import { apiRequest } from '../../api/client.js';

function element(tag, text = '', className = '') {
  const el = document.createElement(tag);
  el.textContent = text;
  if (className) el.className = className;
  return el;
}

function field(label, input) {
  const wrapper = element('label', '', 'appointment-field');
  wrapper.append(element('span', label), input);
  return wrapper;
}

function input(type, value = '') {
  const el = document.createElement('input');
  el.type = type;
  el.value = value;
  return el;
}

export async function renderAppointmentScheduling(
  screen,
  ticketId,
  onBack
) {
  screen.replaceChildren();

  const heading = element('div', '', 'crm-page-heading');
  const headingText = element('div');
  headingText.append(
    element('h2', 'Đặt lịch hẹn'),
    element(
      'p',
      'Lên lịch giao hoặc nhận máy cho phiếu sửa chữa'
    )
  );

  const backButton = element('button', '← Quay lại', 'crm-outline');
  backButton.type = 'button';
  backButton.onclick = onBack;
  heading.append(headingText, backButton);
  screen.append(heading);

  const panel = element('section', '', 'crm-panel appointment-panel');
  const loading = element('p', 'Đang tải thông tin phiếu...');
  panel.append(loading);
  screen.append(panel);

  let context;

  try {
    context = await apiRequest(
      `/appointments/context/${encodeURIComponent(ticketId)}`
    );
  } catch (error) {
    loading.textContent = error.message;
    return;
  }

  panel.replaceChildren();

  panel.append(
    element('h3', 'Thông tin lịch hẹn'),
    element(
      'p',
      'Thời lượng mỗi lịch hẹn là 60 phút. Hệ thống kiểm tra trùng lịch theo kỹ thuật viên.'
    )
  );

  const form = element('form', '', 'appointment-form');

  const ticketInput = input(
    'text',
    `#${context.ticket_id} – ${context.title}`
  );
  ticketInput.readOnly = true;

  const technicianInput = input(
    'text',
    context.technician_name || 'Chưa phân công'
  );
  technicianInput.readOnly = true;

  const typeSelect = document.createElement('select');

  [
    ['DELIVERY', 'Giao máy'],
    ['PICKUP', 'Nhận máy'],
  ].forEach(([value, label]) => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = label;
    typeSelect.append(option);
  });

  const dateInput = input('date');
  dateInput.required = true;

  const timeInput = input('time', '09:00');
  timeInput.required = true;
  timeInput.step = 60;

  const statusInput = input('text', 'SCHEDULED – Đã lên lịch');
  statusInput.readOnly = true;

  form.append(
    field('Mã phiếu sửa chữa', ticketInput),
    field('Kỹ thuật viên phụ trách', technicianInput),
    field('Loại lịch hẹn', typeSelect),
    field('Ngày hẹn', dateInput),
    field('Giờ bắt đầu', timeInput),
    field('Trạng thái', statusInput)
  );

  const result = element(
    'p',
    'Vui lòng chọn ngày và giờ hẹn.',
    'appointment-result'
  );
  result.setAttribute('role', 'status');

  const actions = element('div', '', 'wf-actions');

  const checkButton = element(
    'button',
    'Kiểm tra trùng lịch',
    'crm-outline'
  );
  checkButton.type = 'button';

  const saveButton = element(
    'button',
    'Xác nhận đặt lịch',
    'crm-primary'
  );
  saveButton.type = 'submit';

  const cancelButton = element(
    'button',
    'Hủy',
    'crm-outline'
  );
  cancelButton.type = 'button';
  cancelButton.onclick = onBack;

  actions.append(checkButton, saveButton, cancelButton);

  panel.append(form, result);
  form.append(actions);

  if (
    context.ticket_status !== 'ASSIGNED' ||
    !context.technician_id
  ) {
    checkButton.disabled = true;
    saveButton.disabled = true;
    result.textContent =
      'Chỉ có thể đặt lịch cho phiếu đang được phân công kỹ thuật viên.';
    return;
  }


  function clearFieldError(control) {
    control.classList.remove('appointment-input-error');
    control.removeAttribute('aria-invalid');

    const message = control.parentElement.querySelector(
      '.appointment-field-error'
    );
    if (message) message.remove();
  }

  function showFieldError(control, message) {
    clearFieldError(control);

    control.classList.add('appointment-input-error');
    control.setAttribute('aria-invalid', 'true');

    const error = element(
      'span',
      message,
      'appointment-field-error'
    );
    control.parentElement.append(error);
  }

  function validateFields() {
    let valid = true;

    clearFieldError(dateInput);
    clearFieldError(timeInput);

    if (!dateInput.value) {
      showFieldError(dateInput, 'Vui lòng chọn ngày hẹn.');
      valid = false;
    }

    if (!timeInput.value) {
      showFieldError(timeInput, 'Vui lòng chọn giờ hẹn.');
      valid = false;
    }

    return valid;
  }

  let checkedPayload = null;

  function getPayload() {
    if (!dateInput.value || !timeInput.value) {
      throw new Error('Vui lòng chọn đầy đủ ngày và giờ hẹn.');
    }

    return {
      ticket_id: Number(context.ticket_id),
      appointment_type: typeSelect.value,
      start_time: `${dateInput.value}T${timeInput.value}:00`,
    };
  }

  function invalidate() {
    checkedPayload = null;
    result.textContent = 'Thông tin đã thay đổi. Hãy kiểm tra lại lịch.';
    result.className = 'appointment-result';
  }

  [dateInput, timeInput].forEach((control) => {
    control.addEventListener('input', () => clearFieldError(control));
    control.addEventListener('change', () => clearFieldError(control));
  });

  [typeSelect, dateInput, timeInput].forEach((control) => {
    control.addEventListener('change', invalidate);
    control.addEventListener('input', invalidate);
  });

  checkButton.onclick = async () => {
    if (!validateFields()) {
      result.textContent = 'Vui lòng hoàn thành các trường bắt buộc.';
      result.className = 'appointment-result appointment-error';
      return;
    }

    checkButton.disabled = true;
    result.textContent = 'Đang kiểm tra lịch...';

    try {
      const payload = getPayload();
      const response = await apiRequest('/appointments/check', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      if (response.available) {
        checkedPayload = JSON.stringify(payload);
        result.textContent =
          'Không có xung đột lịch. Có thể xác nhận đặt lịch.';
        result.className = 'appointment-result appointment-success';
      } else {
        checkedPayload = null;
        result.textContent =
          'Kỹ thuật viên đã có lịch hẹn trùng thời gian.';
        result.className = 'appointment-result appointment-error';
      }
    } catch (error) {
      checkedPayload = null;
      result.textContent = error.message;
      result.className = 'appointment-result appointment-error';
    } finally {
      checkButton.disabled = false;
    }
  };

  form.noValidate = true;

  form.onsubmit = async (event) => {
    event.preventDefault();

    if (!validateFields()) {
      result.textContent = 'Vui lòng hoàn thành các trường bắt buộc.';
      result.className = 'appointment-result appointment-error';
      return;
    }

    let payload;

    try {
      payload = getPayload();
    } catch (error) {
      result.textContent = error.message;
      return;
    }

    if (JSON.stringify(payload) !== checkedPayload) {
      result.textContent =
        'Vui lòng kiểm tra trùng lịch trước khi xác nhận.';
      return;
    }

    saveButton.disabled = true;
    result.textContent = 'Đang lưu lịch hẹn...';

    try {
      const saved = await apiRequest('/appointments', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      result.replaceChildren();

      const successTitle = document.createElement('strong');
      successTitle.textContent = '✓ Đặt lịch hẹn thành công!';

      const successDetail = document.createElement('span');
      successDetail.textContent =
        `Lịch hẹn #${saved.appointment_id} đã được lưu. ` +
        'Bạn có thể xem lại trong mục Lịch hẹn.';

      result.append(successTitle, successDetail);
      result.className =
        'appointment-result appointment-success appointment-confirmation';
      result.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
      });
      checkedPayload = null;
      checkButton.disabled = true;
      saveButton.disabled = true;
    } catch (error) {
      result.textContent = error.message;
      result.className = 'appointment-result appointment-error';
      saveButton.disabled = false;
    }
  };
}
