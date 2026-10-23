
import './style.css';
import { getTickets } from '../api/ticket.api.js';
import { renderTicketDetail } from './pages/TicketDetail.js';
import { renderTechnicianAssignment } from './pages/TechnicianAssignment.js';

const app = document.querySelector('#app');

app.innerHTML = `
  <main class="container">
    <header>
      <h1>Smart CRM – Mekong Mobile</h1>
      <p>Quản lý phân công kỹ thuật viên – Luồng L4</p>
    </header>

    <section id="screen" aria-live="polite"></section>
  </main>
`;

const screen = document.querySelector('#screen');

function showMessage(container, message) {
  container.replaceChildren();

  const paragraph = document.createElement('p');
  paragraph.textContent = message;
  container.appendChild(paragraph);
}

function createTicketCard(ticket) {
  const card = document.createElement('article');
  card.className = 'ticket-card';

  const title = document.createElement('h3');
  title.textContent = `#${ticket.ticket_id} – ${ticket.title}`;

  const details = document.createElement('p');
  details.textContent =
    `Nhóm lỗi: ${ticket.incident_group} | ` +
    `Ưu tiên: ${ticket.priority} | ` +
    `Trạng thái: ${ticket.status}`;

  const center = document.createElement('p');
  center.textContent = `Trung tâm: ${ticket.center_id}`;

  // Màn hình 2: Chi tiết phiếu
  const detailButton = document.createElement('button');
  detailButton.type = 'button';
  detailButton.textContent = 'Xem chi tiết';

  detailButton.addEventListener('click', () => {
    renderTicketDetail(
      screen,
      ticket.ticket_id,
      renderTicketList
    );
  });

  // Màn hình 3: Phân công kỹ thuật viên
  const assignButton = document.createElement('button');
  assignButton.type = 'button';
  assignButton.textContent = 'Phân công kỹ thuật viên';

  // Chỉ cho phép phân công khi phiếu đang PENDING
  // và chưa có kỹ thuật viên phụ trách.
  assignButton.disabled =
    ticket.status !== 'PENDING' ||
    ticket.is_assigned === true;

  if (ticket.is_assigned === true) {
    assignButton.textContent = 'Đã phân công';
  }

  assignButton.addEventListener('click', () => {
    if (assignButton.disabled) {
      return;
    }

    renderTechnicianAssignment(
      screen,
      ticket.ticket_id,
      renderTicketList
    );
  });

  card.append(
    title,
    details,
    center,
    detailButton,
    assignButton
  );

  return card;
}

async function renderTicketList() {
  screen.replaceChildren();

  const heading = document.createElement('h2');
  heading.textContent = 'Danh sách phiếu sửa chữa';

  const reloadButton = document.createElement('button');
  reloadButton.type = 'button';
  reloadButton.textContent = 'Tải lại';

  const ticketList = document.createElement('div');
  ticketList.id = 'ticket-list';
  ticketList.setAttribute('aria-live', 'polite');

  screen.append(heading, reloadButton, ticketList);

  async function loadTickets() {
    showMessage(ticketList, 'Đang tải danh sách phiếu...');
    reloadButton.disabled = true;

    try {
      const tickets = await getTickets();

      if (!Array.isArray(tickets)) {
        throw new Error(
          'Dữ liệu API không đúng định dạng danh sách.'
        );
      }

      ticketList.replaceChildren();

      if (tickets.length === 0) {
        showMessage(
          ticketList,
          'Hiện chưa có phiếu sửa chữa.'
        );
        return;
      }

      tickets.forEach((ticket) => {
        ticketList.appendChild(createTicketCard(ticket));
      });
    } catch (error) {
      showMessage(
        ticketList,
        `Không thể tải dữ liệu: ${error.message}`
      );
    } finally {
      reloadButton.disabled = false;
    }
  }

  reloadButton.addEventListener('click', loadTickets);

  await loadTickets();
}

// Khởi động màn hình danh sách phiếu
renderTicketList();
