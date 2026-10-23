
import {
  getEligibleTechnicians,
  assignTechnician,
} from '../../api/ticket.api.js';

export async function renderTechnicianAssignment(
  container,
  ticketId,
  onBack
) {
  container.replaceChildren();

  const heading = document.createElement('h2');
  heading.textContent = `Phân công kỹ thuật viên – Phiếu #${ticketId}`;

  const backButton = document.createElement('button');
  backButton.type = 'button';
  backButton.textContent = '← Quay lại danh sách';
  backButton.addEventListener('click', onBack);

  const content = document.createElement('div');
  content.id = 'assignment-content';
  content.setAttribute('aria-live', 'polite');

  container.append(heading, backButton, content);

  function showMessage(message) {
    content.replaceChildren();

    const paragraph = document.createElement('p');
    paragraph.textContent = message;

    content.appendChild(paragraph);
  }

  async function loadTechnicians() {
    showMessage('Đang tải kỹ thuật viên phù hợp...');

    try {
      const technicians = await getEligibleTechnicians(ticketId);

      if (!Array.isArray(technicians)) {
        throw new Error(
          'Dữ liệu kỹ thuật viên không đúng định dạng.'
        );
      }

      content.replaceChildren();

      if (technicians.length === 0) {
        showMessage('Không có kỹ thuật viên đủ điều kiện.');
        return;
      }

      technicians.forEach((technician) => {
        const card = document.createElement('article');
        card.className = 'ticket-card';

        const name = document.createElement('h3');
        name.textContent =
          technician.name ??
          `Kỹ thuật viên #${technician.technician_id}`;

        const details = document.createElement('p');
        details.textContent =
          `Mã KTV: ${technician.technician_id} | ` +
          `Trạng thái: ${technician.availability_status ?? 'Chưa có'} | ` +
          `Nhóm kỹ năng: ${technician.incident_group ?? 'Chưa có'} | ` +
          `Khu vực: ${technician.area ?? 'Chưa có'} | ` +
          `Trung tâm: ${technician.center_id ?? 'Chưa có'} | ` +
          `Tay nghề: ${technician.proficiency ?? 'Chưa có'} | ` +
          `Số phiếu đang phụ trách: ${technician.current_workload ?? 0}`;

        const assignButton = document.createElement('button');
        assignButton.type = 'button';
        assignButton.textContent = 'Phân công';

        const feedback = document.createElement('p');
        feedback.setAttribute('role', 'status');

        assignButton.addEventListener('click', async () => {
          const allButtons = content.querySelectorAll('button');

          allButtons.forEach((button) => {
            button.disabled = true;
          });

          assignButton.textContent = 'Đang phân công...';
          feedback.textContent = '';

          try {
            await assignTechnician(
              ticketId,
              technician.technician_id
            );

            showMessage(
              `Phân công thành công! Phiếu #${ticketId} ` +
              `đã được giao cho ${technician.name ?? `KTV #${technician.technician_id}`}.`
            );
          } catch (error) {
            feedback.textContent =
              `Không thể phân công: ${error.message}`;

            allButtons.forEach((button) => {
              button.disabled = false;
            });

            assignButton.textContent = 'Phân công';
          }
        });

        card.append(name, details, assignButton, feedback);
        content.appendChild(card);
      });
    } catch (error) {
      showMessage(
        `Không thể tải kỹ thuật viên: ${error.message}`
      );
    }
  }

  await loadTechnicians();
}
