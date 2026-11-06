import { getTicketById, getReassignmentCandidates, reassignTechnician } from '../../api/ticket.api.js';
import { getCurrentUser } from '../auth.js';
import { apiRequest } from '../../api/client.js';

function el(tag, text = '', className = '') {
  const item = document.createElement(tag);
  item.textContent = String(text ?? '');
  if (className) item.className = className;
  return item;
}

function info(label, value) {
  const item = el('div', '', 'detail-info-item');
  item.append(
    el('span', label, 'detail-info-label'),
    el('strong', value ?? 'Chưa có', 'detail-info-value')
  );
  return item;
}

function formatDate(value) {
  if (!value) return 'Chưa có';
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleString('vi-VN', {
        timeZone: 'Asia/Ho_Chi_Minh',
        hour12: false,
      });
}

const statusLabels = {
  PENDING: 'Chờ phân công',
  ASSIGNED: 'Đã phân công',
  COMPLETED: 'Đã hoàn thành',
};

export async function renderTicketDetail(container, ticketId, onBack) {
  container.replaceChildren();

  const heading = el('div', '', 'detail-page-heading');
  const headingContent = el('div');
  headingContent.append(
    el('span', 'QUẢN LÝ PHIẾU / CHI TIẾT', 'detail-eyebrow'),
    el('h2', `Chi tiết phiếu #${ticketId}`)
  );

  const back = el('button', '← Quay lại danh sách', 'crm-outline');
  back.type = 'button';
  back.addEventListener('click', onBack);

  heading.append(headingContent, back);

  const content = el(
    'div',
    'Đang tải thông tin phiếu...',
    'detail-page-content'
  );

  container.append(heading, content);

  try {
    const [ticket, assignmentData] = await Promise.all([
      getTicketById(ticketId),
      apiRequest(`/assignments/ticket/${ticketId}/detail`),
    ]);

    if (!ticket?.ticket_id) {
      throw new Error('Không tìm thấy thông tin phiếu.');
    }

    content.replaceChildren();

    const overview = el('section', '', 'detail-card');
    const overviewHeader = el('div', '', 'detail-card-header');
    const overviewTitle = el('div');

    overviewTitle.append(
      el('span', 'THÔNG TIN PHIẾU', 'detail-eyebrow'),
      el('h3', ticket.title || `Phiếu #${ticket.ticket_id}`)
    );

    const status = el(
      'span',
      statusLabels[ticket.status] || ticket.status,
      `detail-status detail-status-${String(ticket.status).toLowerCase()}`
    );

    overviewHeader.append(overviewTitle, status);

    const overviewGrid = el('div', '', 'detail-info-grid');

    overviewGrid.append(
      info('Mã phiếu', `#${ticket.ticket_id}`),
      info('Nhóm lỗi', ticket.incident_group),
      info('Mức ưu tiên', ticket.priority),
      info('Trung tâm', `Trung tâm #${ticket.center_id}`)
    );

    overview.append(overviewHeader, overviewGrid);

    const technicianCard = el('section', '', 'detail-card');
    technicianCard.append(
      el('span', 'PHÂN CÔNG KỸ THUẬT VIÊN', 'detail-eyebrow'),
      el('h3', 'Kỹ thuật viên phụ trách')
    );

    const assignment = assignmentData?.assignment;

    if (!assignment) {
      technicianCard.append(
        el(
          'div',
          'Chưa có kỹ thuật viên phụ trách phiếu này.',
          'detail-empty'
        )
      );
    } else {
      const profile = el('div', '', 'detail-technician-profile');
      const avatar = el(
        'div',
        (assignment.technician_name || 'KT')
          .split(/\s+/)
          .slice(-2)
          .map((word) => word.charAt(0))
          .join('')
          .toUpperCase(),
        'detail-technician-avatar'
      );

      const identity = el('div', '', 'detail-technician-identity');
      identity.append(
        el('strong', assignment.technician_name),
        el(
          'span',
          `Kỹ thuật viên #${assignment.technician_id}`,
          'detail-info-label'
        )
      );

      const assignmentBadge = el(
        'span',
        assignment.ended_at
          ? 'Đã kết thúc phân công'
          : 'Đang phụ trách',
        assignment.ended_at
          ? 'detail-status'
          : 'detail-status detail-status-assigned'
      );

      profile.append(avatar, identity, assignmentBadge);

      const technicianGrid = el('div', '', 'detail-info-grid');
      technicianGrid.append(
        info('Mã kỹ thuật viên', `#${assignment.technician_id}`),
        info('Khu vực phụ trách', assignment.technician_area || 'Chưa cập nhật'),
        info('Trung tâm', `Trung tâm #${assignment.technician_center_id}`),
        info('Trạng thái khả dụng', assignment.availability_status),
        info('Thời gian phân công', formatDate(assignment.assigned_at))
      );

      if (assignment.ended_at) {
        technicianGrid.append(
          info('Kết thúc phân công', formatDate(assignment.ended_at))
        );
      }

      technicianCard.append(profile, technicianGrid);
    }



    // BUG-02: Assignment history UI
    const historyUser = await getCurrentUser();

    if (historyUser?.role === 'MANAGER') {
      const historyCard = el('section', '', 'detail-card');

      historyCard.append(
        el('span', 'LỊCH SỬ PHÂN CÔNG', 'detail-eyebrow'),
        el('h3', 'Các lần phân công kỹ thuật viên')
      );

      try {
        const history = await apiRequest(
          `/assignments/ticket/${encodeURIComponent(ticketId)}/history`
        );

        if (!history.length) {
          historyCard.append(
            el('p', 'Chưa có lịch sử phân công.', 'detail-empty')
          );
        } else {
          const wrapper = el('div');
          wrapper.style.overflowX = 'auto';

          const table = document.createElement('table');
          table.style.width = '100%';
          table.style.borderCollapse = 'collapse';
          table.style.marginTop = '16px';

          const thead = document.createElement('thead');
          const headerRow = document.createElement('tr');

          for (const label of [
            'Kỹ thuật viên',
            'Bắt đầu',
            'Kết thúc',
            'Lý do thay đổi',
            'Trạng thái'
          ]) {
            const th = el('th', label);
            th.style.padding = '12px';
            th.style.textAlign = 'left';
            th.style.borderBottom = '1px solid #ddd';
            headerRow.append(th);
          }

          thead.append(headerRow);
          table.append(thead);

          const tbody = document.createElement('tbody');

          for (const item of history) {
            const tr = document.createElement('tr');

            const values = [
              `${item.technician_name} (#${item.technician_id})`,
              formatDate(item.assigned_at),
              item.ended_at ? formatDate(item.ended_at) : '—',
              item.change_reason || '—',
              item.ended_at ? 'Đã kết thúc' : 'Đang phụ trách'
            ];

            for (const value of values) {
              const td = el('td', value);
              td.style.padding = '12px';
              td.style.borderBottom = '1px solid #eee';
              td.style.verticalAlign = 'top';
              tr.append(td);
            }

            tbody.append(tr);
          }

          table.append(tbody);
          wrapper.append(table);
          historyCard.append(wrapper);
        }
      } catch (error) {
        historyCard.append(
          el(
            'p',
            `Không thể tải lịch sử phân công: ${error.message}`,
            'detail-empty'
          )
        );
      }

      content.append(historyCard);
    }

    // BUG-02: Reassignment form
    const currentUser = await getCurrentUser();

    if (
      currentUser?.role === 'MANAGER' &&
      ticket.status === 'ASSIGNED' &&
      assignment &&
      !assignment.ended_at
    ) {
      const formCard = el('section', '', 'detail-card');
      formCard.append(
        el('span', 'ĐIỀU CHỈNH PHÂN CÔNG', 'detail-eyebrow'),
        el('h3', 'Đổi kỹ thuật viên phụ trách')
      );

      const form = document.createElement('form');
      form.style.display = 'grid';
      form.style.gap = '12px';

      const technicianLabel = el('label', 'Kỹ thuật viên mới');
      const technicianSelect = document.createElement('select');
      technicianSelect.required = true;
      technicianSelect.style.padding = '12px';
      technicianSelect.style.width = '100%';

      const reasonLabel = el('label', 'Lý do thay đổi');
      const reasonInput = document.createElement('textarea');
      reasonInput.required = true;
      reasonInput.maxLength = 255;
      reasonInput.rows = 3;
      reasonInput.placeholder = 'Nhập lý do đổi kỹ thuật viên...';
      reasonInput.style.padding = '12px';
      reasonInput.style.width = '100%';

      const message = el('p', '');
      message.setAttribute('role', 'status');

      const submit = el('button', 'Xác nhận đổi kỹ thuật viên', 'crm-primary');
      submit.type = 'submit';

      form.append(
        technicianLabel,
        technicianSelect,
        reasonLabel,
        reasonInput,
        message,
        submit
      );

      formCard.append(form);

      try {
        const candidates = await getReassignmentCandidates(ticketId);

        technicianSelect.replaceChildren();

        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Chọn kỹ thuật viên đủ điều kiện';
        technicianSelect.append(placeholder);

        for (const technician of candidates) {
          const option = document.createElement('option');
          option.value = String(technician.technician_id);
          option.textContent =
            `${technician.name} (#${technician.technician_id})`;
          technicianSelect.append(option);
        }

        if (candidates.length === 0) {
          message.textContent = 'Không có kỹ thuật viên đủ điều kiện.';
          submit.disabled = true;
        }
      } catch (error) {
        message.textContent =
          `Không thể tải danh sách kỹ thuật viên: ${error.message}`;
        submit.disabled = true;
      }

      form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const technicianId = Number(technicianSelect.value);
        const reason = reasonInput.value.trim();

        if (!technicianId || !reason) {
          message.textContent =
            'Vui lòng chọn kỹ thuật viên và nhập lý do thay đổi.';
          return;
        }

        submit.disabled = true;
        message.textContent = 'Đang cập nhật phân công...';

        try {
          await reassignTechnician(ticketId, technicianId, reason);
          await renderTicketDetail(container, ticketId, onBack);
        } catch (error) {
          message.textContent = `Đổi kỹ thuật viên thất bại: ${error.message}`;
          submit.disabled = false;
        }
      });

      content.append(overview, technicianCard, formCard);
    } else {
      content.append(overview, technicianCard);
    }

  } catch (error) {
    content.replaceChildren(
      el(
        'div',
        `Không thể tải chi tiết phiếu: ${error.message}`,
        'detail-empty'
      )
    );

    const retry = el('button', 'Thử lại', 'crm-primary');
    retry.type = 'button';
    retry.addEventListener('click', () =>
      renderTicketDetail(container, ticketId, onBack)
    );

    content.append(retry);
  }
}
