
import { getTicketById } from '../../api/ticket.api.js';

export async function renderTicketDetail(container, ticketId, onBack) {
  container.replaceChildren();

  const heading = document.createElement('h2');
  heading.textContent = `Chi tiết phiếu #${ticketId}`;

  const backButton = document.createElement('button');
  backButton.type = 'button';
  backButton.textContent = '← Quay lại danh sách';
  backButton.addEventListener('click', onBack);

  const content = document.createElement('div');
  content.className = 'ticket-detail';
  content.setAttribute('aria-live', 'polite');
  content.textContent = 'Đang tải chi tiết phiếu...';

  container.append(heading, backButton, content);

  try {
    const ticket = await getTicketById(ticketId);

    if (!ticket || !ticket.ticket_id) {
      throw new Error('Không tìm thấy thông tin phiếu.');
    }

    const fields = [
      ['Mã phiếu', ticket.ticket_id],
      ['Tiêu đề', ticket.title],
      ['Nhóm lỗi', ticket.incident_group],
      ['Mức ưu tiên', ticket.priority],
      ['Trạng thái', ticket.status],
      ['Trung tâm', ticket.center_id],
    ];

    content.replaceChildren();

    fields.forEach(([label, value]) => {
      const paragraph = document.createElement('p');

      const strong = document.createElement('strong');
      strong.textContent = `${label}: `;

      const span = document.createElement('span');
      span.textContent = String(value ?? 'Chưa có');

      paragraph.append(strong, span);
      content.appendChild(paragraph);
    });
  } catch (error) {
    content.textContent = `Không thể tải chi tiết phiếu: ${error.message}`;
  }
}
