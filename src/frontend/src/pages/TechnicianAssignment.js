import {
  getTicketById,
  getEligibleTechnicians,
  assignTechnician,
} from '../../api/ticket.api.js';

export async function renderTechnicianAssignment(container, ticketId, onBack) {
  container.replaceChildren();

  const heading = document.createElement('h2');
  heading.textContent = `Phân công kỹ thuật viên – Phiếu #${ticketId}`;

  const content = document.createElement('div');
  content.id = 'assignment-content';
  content.setAttribute('aria-live', 'polite');

  container.append(heading, content);

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (className) node.className = className;
    return node;
  }

  function showMessage(message) {
    content.replaceChildren(element('p', message));
  }

  function createTable(headers) {
    const table = element('table', undefined, 'wf-table');
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    headers.forEach((label) => {
      headerRow.appendChild(element('th', label));
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);
    return table;
  }

  async function loadAssignment() {
    showMessage('Đang tải thông tin phiếu và kỹ thuật viên...');

    try {
      const [ticket, technicians] = await Promise.all([
        getTicketById(ticketId),
        getEligibleTechnicians(ticketId),
      ]);

      if (!Array.isArray(technicians)) {
        throw new Error('Dữ liệu kỹ thuật viên không đúng định dạng.');
      }

      content.replaceChildren();

      // A. Thông tin phiếu được chọn
      content.appendChild(element('h3', 'A. THÔNG TIN PHIẾU ĐƯỢC CHỌN'));

      const ticketInfo = element('div', undefined, 'wf-info');
      ticketInfo.textContent =
        `Phiếu #${ticket.ticket_id} | ${ticket.title} | ` +
        `Nhóm lỗi: ${ticket.incident_group} | ` +
        `Ưu tiên: ${ticket.priority} | ` +
        `Trạng thái: ${ticket.status} | ` +
        `Trung tâm: ${ticket.center_id}`;

      content.appendChild(ticketInfo);

      // B. Danh sách kỹ thuật viên khả dụng
      content.appendChild(element('h3', 'B. DANH SÁCH KỸ THUẬT VIÊN KHẢ DỤNG'));

      if (technicians.length === 0) {
        content.appendChild(element('p', 'Không có kỹ thuật viên đủ điều kiện.'));
        const back = element('button', 'Hủy');
        back.addEventListener('click', onBack);
        content.appendChild(back);
        return;
      }

      const wrapper = element('div', undefined, 'wf-table-wrap');
      const table = createTable([
        'Chọn',
        'Kỹ thuật viên',
        'Khu vực',
        'Khả dụng',
        'Workload',
        'Nhóm sự cố',
        'Tay nghề',
        'Trung tâm',
      ]);

      const tbody = document.createElement('tbody');
      let selectedTechnician = null;

      const conditions = element('div', undefined, 'wf-info');
      const confirmButton = element('button', 'Xác nhận phân công');
      confirmButton.disabled = true;

      function updateConditions(technician) {
        selectedTechnician = technician;

        const sameCenter =
          Number(technician.center_id) === Number(ticket.center_id);
        const available = technician.availability_status === 'AVAILABLE';
        const sameSkill =
          technician.incident_group === ticket.incident_group;

        conditions.replaceChildren();

        conditions.appendChild(
          element('p', `${available ? '✓' : '✗'} Kỹ thuật viên khả dụng`)
        );
        conditions.appendChild(
          element('p', `${sameCenter ? '✓' : '✗'} Cùng trung tâm`)
        );
        conditions.appendChild(
          element('p', `${sameSkill ? '✓' : '✗'} Phù hợp nhóm sự cố`)
        );

        const proficiencyOK = Number(technician.proficiency) >= 3;

        conditions.appendChild(
          element(
            'p',
            `${proficiencyOK ? '✓' : '✗'} Tay nghề đạt yêu cầu (${technician.proficiency} ≥ 3)`
          )
        );

        const workloadOK = Number(technician.current_workload ?? 0) < 5;
          conditions.appendChild(
            element('p', `${workloadOK ? '✓' : '✗'} Workload dưới 5/5`)
          );

          const eligible = sameCenter && available && sameSkill && proficiencyOK && workloadOK;
        conditions.appendChild(
          element(
            'strong',
            eligible
              ? 'KẾT QUẢ: Đủ điều kiện sơ bộ để phân công'
              : 'KẾT QUẢ: Chưa đủ điều kiện'
          )
        );

        confirmButton.disabled = !eligible;
      }

      technicians.forEach((technician) => {
        const tr = document.createElement('tr');
        const selectCell = document.createElement('td');
        const radio = document.createElement('input');

        radio.type = 'radio';
        radio.name = 'selected-technician';
        radio.value = technician.technician_id;
        radio.setAttribute(
          'aria-label',
          `Chọn ${technician.name ?? `KTV ${technician.technician_id}`}`
        );

        radio.addEventListener('change', () => {
          updateConditions(technician);
        });

        selectCell.appendChild(radio);
        tr.appendChild(selectCell);

        [
          technician.name ?? `KTV #${technician.technician_id}`,
          technician.area ?? '—',
          technician.availability_status ?? '—',
          `${technician.current_workload ?? 0}/5`,
          technician.incident_group ?? '—',
          technician.proficiency ?? '—',
          technician.center_id ?? '—',
        ].forEach((value) => {
          tr.appendChild(element('td', value));
        });

        tbody.appendChild(tr);
      });

      table.appendChild(tbody);
      wrapper.appendChild(table);
      content.appendChild(wrapper);

      // C. Kiểm tra điều kiện phân công
      content.appendChild(element('h3', 'C. KIỂM TRA ĐIỀU KIỆN PHÂN CÔNG'));
      conditions.textContent = 'Vui lòng chọn kỹ thuật viên để kiểm tra.';
      content.appendChild(conditions);

      const feedback = element('p');
      feedback.setAttribute('role', 'status');

      const actions = element('div', undefined, 'wf-actions');
      const cancelButton = element('button', 'Hủy');

      cancelButton.addEventListener('click', onBack);

      confirmButton.addEventListener('click', async () => {
        if (!selectedTechnician) return;

        confirmButton.disabled = true;
        cancelButton.disabled = true;
        confirmButton.textContent = 'Đang phân công...';
        feedback.textContent = '';

        try {
          await assignTechnician(
            ticketId,
            selectedTechnician.technician_id
          );

          content.replaceChildren(
            element(
              'p',
              `Phân công thành công! Phiếu #${ticketId} đã được giao cho ` +
                `${selectedTechnician.name ?? `KTV #${selectedTechnician.technician_id}`}.`
            )
          );

          const back = element('button', 'Quay lại danh sách');
          back.addEventListener('click', onBack);
          content.appendChild(back);
        } catch (error) {
          feedback.textContent = `Không thể phân công: ${error.message}`;
          confirmButton.disabled = false;
          cancelButton.disabled = false;
          confirmButton.textContent = 'Xác nhận phân công';
        }
      });

      actions.append(confirmButton, cancelButton);
      content.append(actions, feedback);
    } catch (error) {
      showMessage(`Không thể tải dữ liệu phân công: ${error.message}`);

      const retry = element('button', 'Thử lại');
      retry.addEventListener('click', loadAssignment);

      const back = element('button', 'Hủy');
      back.addEventListener('click', onBack);

      content.append(retry, back);
    }
  }

  await loadAssignment();
}
