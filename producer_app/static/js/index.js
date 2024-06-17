const urls = [lineChartUrl,];

Promise.all(urls.map(url => d3.json(url))).then(run);

function run(dataset) {
   d3lineChart(dataset[0]);
};