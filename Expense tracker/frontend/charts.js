window.onload = function () {

  const categoryData = [
    { category: "Food", total: 400 },
    { category: "Transport", total: 250 },
    { category: "Shopping", total: 300 },
    { category: "Bills", total: 150 }
  ];

  const dailyData = [
    { date: "Mon", total: 120 },
    { date: "Tue", total: 200 },
    { date: "Wed", total: 150 },
    { date: "Thu", total: 300 },
    { date: "Fri", total: 180 }
  ];

  const pieCtx = document.getElementById("pieChart");
  const barCtx = document.getElementById("barChart");

  new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: categoryData.map(d => d.category),
      datasets: [{
        data: categoryData.map(d => d.total)
      }]
    }
  });

  new Chart(barCtx, {
    type: "bar",
    data: {
      labels: dailyData.map(d => d.date),
      datasets: [{
        label: "Daily Expense",
        data: dailyData.map(d => d.total)
      }]
    }
  });
};


