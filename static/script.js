<div class="container-fluid">
    <div class="row">
        <div class="col-3"></div>
        <div class="col-9">
            <div class="box">
                <canvas id="lineChart" height="350" width="800" style="position: relative; top: 5vh;"></canvas>
            </div>
        </div>
    </div>
</div>
<script>
    function displayLineChart() {
    var data = {
        labels: {{labels}},
        datasets: [
            {
                label: "Prime and Fibonacci",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: {{data}}
            }
        ]
    };
    var ctx = document.getElementById("lineChart").getContext("2d");
    var options = { };
    var lineChart = new Chart(ctx).Line(data, options);


  }
</script>

    (function() {
  var d3 = Plotly.d3;
  var WIDTH_IN_PERCENT_OF_PARENT = 100,
      HEIGHT_IN_PERCENT_OF_PARENT = 90;

  var gd3 = d3.selectAll(".responsive-plot")
        .style({
          width: 'fit-content',
          'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

          height: 'fit-content',
          'margin-top': '0vh'
        });

  var nodes_to_resize = gd3[0]; //not sure why but the goods are within a nested array
  window.onresize = function() {
    for (var i = 0; i < nodes_to_resize.length; i++) {
      Plotly.Plots.resize(nodes_to_resize[i]);
    }
  };

})();


//////////////////////////////////////////////////////////////////////////////////

var trace1 = {
    x: {{labels}},
    y: {{data1}},

    mode: 'line',
    line: {
    width: 2
  }
};
var trace2 = {
    x: {{labels}},
    y: {{data2}},

    mode: 'line',
    line: {
    width: 2
  }
};
var trace3 = {
    x: {{labels}},
    y: {{data3}},

    mode: 'line',
    line: {
    width: 2
  }
};
var trace4 = {
    x: {{labels}},
    y: {{data4}},

    mode: 'line',
    line: {
    width: 2
  }
};
var data_ = [trace1, trace2, trace3, trace4];
var data1_ = [trace1, trace2, trace3, trace4];
var layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: {
                tickfont: {
                  family: 'Old Standard TT, serif',
                  size: 14,
                  color: 'rgb(255, 255, 255)'
                },
                zerolinecolor: 'rgb(255, 255, 255)',
                zerolinewidth: 3,
                gridcolor: 'rgb(105,105,105)',
                tickcolor: 'rgb(255, 255, 255)'
              },
              yaxis: {
                 tickfont: {
                  family: 'Old Standard TT, serif',
                  size: 14,
                  color: 'rgb(255, 255, 255)'
                },
                tickcolor: 'rgb(255, 255, 255)',
                gridcolor: 'rgb(105,105,105)',
                zerolinecolor: 'rgb(255, 255, 255)',
                zerolinewidth: 5
              }
};
var config = {responsive: true};
LINEPLOT1 = document.getElementById('linePlot1');
LINEPLOT2 = document.getElementById('linePlot2');
LINEPLOT3 = document.getElementById('linePlot3');
LINEPLOT4 = document.getElementById('linePlot4');
LINEPLOT5 = document.getElementById('linePlot5');
LINEPLOT6 = document.getElementById('linePlot6');
Plotly.newPlot(LINEPLOT1, data_, layout, config);
Plotly.newPlot(LINEPLOT2, data_, layout, config);
Plotly.newPlot(LINEPLOT3, data_, layout, config);
Plotly.newPlot(LINEPLOT4, data_, layout, config);
Plotly.newPlot(LINEPLOT5, data_, layout, config);
Plotly.newPlot(LINEPLOT6, data_, layout, config);