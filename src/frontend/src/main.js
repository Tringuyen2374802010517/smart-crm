import './style.css';
import { getTickets } from '../api/ticket.api.js';
import { renderTicketDetail } from './pages/TicketDetail.js';
import { renderTechnicianAssignment } from './pages/TechnicianAssignment.js';

const app = document.querySelector('#app');

app.innerHTML = `
  <div class="crm-layout">
    <aside class="crm-sidebar">
      <div class="crm-brand">
        <div class="brand-icon">M</div>
        <div>
          <strong>Mekong Mobile</strong>
          <small>SMART CRM</small>
        </div>
      </div>

      <div class="sidebar-label">WORKSPACE</div>
      <nav class="crm-nav">
        <button id="nav-dashboard" class="nav-item" type="button">
          ◫ &nbsp; Tổng quan
        </button>
        <button id="nav-tickets" class="nav-item active" type="button">
          ▤ &nbsp; Quản lý phiếu
        </button>
      </nav>


      <div class="sidebar-bottom">
        <div class="avatar">QL</div>
        <div>
          <strong>Quản lý trung tâm</strong>
          <small>Smart CRM · L4</small>
        </div>
      </div>
    </aside>

    <div class="crm-main">
      <header class="crm-topbar">
        <div>
          <span class="topbar-label">WORKSPACE / LUỒNG L4</span>
          <h1>Quản lý phân công kỹ thuật viên</h1>
        </div>
      </header>

      <main class="crm-content">
        <div id="screen" aria-live="polite"></div>
      </main>
    </div>
  </div>
`;

const screen = document.querySelector('#screen');
const navTickets = document.querySelector('#nav-tickets');
const navDashboard = document.querySelector('#nav-dashboard');

function node(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = String(text);
  if (className) element.className = className;
  return element;
}

function setNavigation(active) {
  navTickets.classList.toggle('active', active === 'tickets');
  navDashboard.classList.toggle('active', active === 'dashboard');
}

function statusBadge(value) {
  const badge = node('span', value ?? 'UNKNOWN', 'crm-status');
  const status = String(value ?? '').toUpperCase();

  if (status === 'PENDING') badge.classList.add('status-pending');
  else if (status === 'ASSIGNED') badge.classList.add('status-assigned');
  else badge.classList.add('status-other');

  return badge;
}

function priorityBadge(value) {
  const badge = node('span', value ?? '—', 'crm-priority');
  const priority = String(value ?? '').toUpperCase();

  if (priority === 'HIGH' || priority === 'URGENT') {
    badge.classList.add('priority-high');
  }
  return badge;
}

function makeButton(label, handler, className = '') {
  const button = node('button', label, className);
  button.type = 'button';
  button.addEventListener('click', handler);
  return button;
}

function openTicketDetail(ticketId) {
  setNavigation('tickets');
  renderTicketDetail(screen, ticketId, renderTicketList);
}

function openAssignment(ticketId) {
  setNavigation('tickets');
  renderTechnicianAssignment(screen, ticketId, renderTicketList);
}

function makeStat(label, value, icon, color) {
  const card = node('div', undefined, 'crm-stat');
  const iconBox = node('div', icon, `stat-icon ${color}`);
  const content = node('div');
  content.append(
    node('p', label),
    node('strong', value)
  );
  card.append(iconBox, content);
  return card;
}

function renderStats(container, tickets) {
  const stats = node('div', undefined, 'crm-stats');
  const pending = tickets.filter(
    t => t.status === 'PENDING' && t.is_assigned === false
  ).length;
  const assigned = tickets.filter(t => t.status === 'ASSIGNED').length;
  const completed = tickets.filter(t => t.status === 'COMPLETED').length;

  stats.append(
    makeStat('Tổng số phiếu', tickets.length, '▤', 'stat-blue'),
    makeStat('Chờ phân công', pending, '◷', 'stat-orange'),
    makeStat('Đã phân công', assigned, '✓', 'stat-green'),
    makeStat('Đã hoàn thành', completed, '✓', 'stat-blue')
  );

  container.appendChild(stats);
}

async function renderTicketList() {
  setNavigation('tickets');
  screen.replaceChildren();

  const heading = node('div', undefined, 'crm-page-heading');
  const headingText = node('div');
  headingText.append(
    node('h2', 'Danh sách phiếu sửa chữa'),
    node('p', 'Theo dõi và phân công kỹ thuật viên cho các phiếu sửa chữa.')
  );

  const reload = makeButton('↻ Tải lại', loadTickets, 'crm-primary');
  heading.append(headingText, reload);

  const statsContainer = node('div');
  const panel = node('div', undefined, 'crm-panel');

  const panelHeader = node('div', undefined, 'crm-panel-header');
  const panelTitle = node('div');
  panelTitle.append(
    node('h3', 'Phiếu cần quản lý'),
    node('p', 'Tìm kiếm, lọc và thao tác trên danh sách phiếu.')
  );

  const filters = node('div', undefined, 'crm-filters');

  const search = document.createElement('input');
  search.type = 'search';
  search.placeholder = 'Tìm kiếm mã phiếu, tiêu đề...';
  search.setAttribute('aria-label', 'Tìm kiếm phiếu');

  const priorityFilter = document.createElement('select');
  priorityFilter.setAttribute('aria-label', 'Lọc mức ưu tiên');

  const statusFilter = document.createElement('select');
  statusFilter.setAttribute('aria-label', 'Lọc trạng thái');

  const tableContainer = node('div', undefined, 'crm-table-scroll');
  const count = node('p', '', 'crm-result-count');

  filters.append(search, priorityFilter, statusFilter);
  panelHeader.append(panelTitle, filters);
  panel.append(panelHeader, tableContainer, count);
  screen.append(heading, statsContainer, panel);

  let allTickets = [];

  function fillSelect(select, placeholder, values) {
    select.replaceChildren();
    const defaultOption = new Option(placeholder, '');
    select.add(defaultOption);

    values.forEach(value => {
      select.add(new Option(value, value));
    });
  }

  function renderRows() {
    const keyword = search.value.trim().toLowerCase();

    const filtered = allTickets.filter(ticket => {
      const text = `${ticket.ticket_id} ${ticket.title ?? ''}`.toLowerCase();

      return text.includes(keyword) &&
        (!priorityFilter.value || ticket.priority === priorityFilter.value) &&
        (!statusFilter.value || ticket.status === statusFilter.value);
    });

    tableContainer.replaceChildren();
    count.textContent = `Hiển thị ${filtered.length} / ${allTickets.length} phiếu`;

    if (filtered.length === 0) {
      tableContainer.append(
        node('div', 'Không tìm thấy phiếu phù hợp với bộ lọc.', 'crm-empty')
      );
      return;
    }

    const table = node('table', undefined, 'crm-data-table');
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');

    [
      'MÃ PHIẾU',
      'TIÊU ĐỀ',
      'NHÓM SỰ CỐ',
      'ƯU TIÊN',
      'TRẠNG THÁI',
      'TRUNG TÂM',
      'THAO TÁC'
    ].forEach(label => {
      headRow.appendChild(node('th', label));
    });

    thead.appendChild(headRow);

    const tbody = document.createElement('tbody');

    filtered.forEach(ticket => {
      const row = document.createElement('tr');

      row.appendChild(node('td', `#${ticket.ticket_id}`, 'ticket-id'));
      row.appendChild(node('td', ticket.title ?? '—', 'ticket-title'));
      row.appendChild(node('td', ticket.incident_group ?? '—'));

      const priorityCell = document.createElement('td');
      priorityCell.appendChild(priorityBadge(ticket.priority));
      row.appendChild(priorityCell);

      const statusCell = document.createElement('td');
      statusCell.appendChild(statusBadge(ticket.status));
      row.appendChild(statusCell);

      row.appendChild(node('td', ticket.center_id ?? '—'));

      const actions = node('td', undefined, 'crm-row-actions');

      const detail = makeButton(
        'Chi tiết',
        () => openTicketDetail(ticket.ticket_id),
        'crm-outline'
      );

      const assign = makeButton(
        'Phân công',
        () => openAssignment(ticket.ticket_id),
        'crm-primary'
      );

      assign.disabled =
        ticket.status !== 'PENDING' ||
        ticket.is_assigned === true;

      if (ticket.is_assigned === true) {
        assign.textContent = 'Đã phân công';
      }

      actions.append(detail, assign);

        if (ticket.status === 'ASSIGNED') {
          const complete = makeButton(
            'Hoàn thành',
            async () => {
              if (!window.confirm(`Xác nhận hoàn thành phiếu #${ticket.ticket_id}?`)) {
                return;
              }

              complete.disabled = true;
              complete.textContent = 'Đang xử lý...';

              try {
                const response = await fetch(
                  `http://127.0.0.1:8000/tickets/${ticket.ticket_id}/complete`,
                  { method: 'PATCH' }
                );

                if (!response.ok) {
                  const data = await response.json().catch(() => ({}));
                  throw new Error(
                    typeof data.detail === 'string'
                      ? data.detail
                      : 'Không thể hoàn thành phiếu.'
                  );
                }

                await loadTickets();
              } catch (error) {
                window.alert(error.message);
                complete.disabled = false;
                complete.textContent = 'Hoàn thành';
              }
            },
            'crm-outline'
          );

          actions.appendChild(complete);
        }
      row.appendChild(actions);
      tbody.appendChild(row);
    });

    table.append(thead, tbody);
    tableContainer.appendChild(table);
  }

  async function loadTickets() {
    tableContainer.replaceChildren(
      node('div', 'Đang tải danh sách phiếu...', 'crm-empty')
    );
    reload.disabled = true;

    try {
      const tickets = await getTickets();

      if (!Array.isArray(tickets)) {
        throw new Error('Dữ liệu API không đúng định dạng.');
      }

      allTickets = tickets;

      statsContainer.replaceChildren();
      renderStats(statsContainer, allTickets);

      fillSelect(
        priorityFilter,
        'Tất cả ưu tiên',
        [...new Set(tickets.map(t => t.priority).filter(Boolean))]
      );

      fillSelect(
        statusFilter,
        'Tất cả trạng thái',
        [...new Set(tickets.map(t => t.status).filter(Boolean))]
      );

      renderRows();
    } catch (error) {
      tableContainer.replaceChildren(
        node('div', `Không thể tải dữ liệu: ${error.message}`, 'crm-empty')
      );
      count.textContent = '';
    } finally {
      reload.disabled = false;
    }
  }

  search.addEventListener('input', renderRows);
  priorityFilter.addEventListener('change', renderRows);
  statusFilter.addEventListener('change', renderRows);

  await loadTickets();
}

async function renderDashboard() {
  setNavigation('dashboard');
  screen.replaceChildren();

  const heading = node('div', undefined, 'crm-page-heading');
  const text = node('div');
  text.append(
    node('h2', 'Tổng quan hoạt động'),
    node('p', 'Theo dõi tình trạng phân công kỹ thuật viên tại trung tâm.')
  );
  heading.appendChild(text);

  const stats = node('div');
  const panel = node('div', undefined, 'crm-panel crm-welcome');
  panel.append(
    node('h3', 'Chào mừng đến Smart CRM'),
    node('p', 'Quản lý phiếu sửa chữa và phân công kỹ thuật viên trong luồng L4.'),
    makeButton('Xem danh sách phiếu →', renderTicketList, 'crm-primary')
  );

  screen.append(heading, stats, panel);

  try {
    const tickets = await getTickets();
    if (!Array.isArray(tickets)) throw new Error('Dữ liệu không hợp lệ');
    renderStats(stats, tickets);
  } catch (error) {
    stats.appendChild(
      node('p', `Không thể tải thống kê: ${error.message}`)
    );
  }
}

navTickets.addEventListener('click', renderTicketList);
navDashboard.addEventListener('click', renderDashboard);

renderTicketList();
