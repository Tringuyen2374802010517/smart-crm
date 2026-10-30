import { getTicketById } from '../../api/ticket.api.js';
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

    content.append(overview, technicianCard);
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
