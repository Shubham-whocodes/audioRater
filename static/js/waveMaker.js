var filePath = '/static/audios/156634610064356_169-tblQuan_226_1.wav';

var metadata = [
  {
    start: 0.3,
    duration: 0.4,
    text: 'label 1'
  }, {
    start: 2,
    duration: 0.5,
    text: 'label 2'
  }
];

var bufferLoader = new waves.loaders.AudioBufferLoader();

// load an audio file
bufferLoader.load(filePath).then(
  function(buffer) {
    // add a try/catch to work around promises error throwing
    try {
      // main function - all subssquent code should be considered inside this function
      // this function receive the buffer as argument
      drawGraph(buffer);
    } catch (err) {
      console.error(err.stack);
    }
  },
  function(err) {
    console.error(err);
  }
);


var graph = waves.ui.timeline()
  .xDomain([0, buffer.duration]) // Set the time domain of the graph
  .width(800) // Sets the graph width in pixels
  .height(200); // Sets the graph height in pixels

// 2. Create the waveform visualizer
// ----------------------------------------
var waveformLayer = waves.ui.waveform()
  // The waveform uses raw data internally, so we pass it the raw `arrayBuffer`
  .data(buffer.getChannelData(0).buffer)
  .sampleRate(buffer.sampleRate)
  .color('#586e75');

// 3. create some segments / labels to display metadata
// ----------------------------------------
var segmentLayer = waves.ui.segment()
  .params({
    interactions: { editable: true },
    opacity: 0.3,
    handlerOpacity: 0.5 // handlers opacity are higher to see them with ease
  })
  .data(metadata)
  .color('#cb4b16');

var labelLayer = waves.ui.label()
  .data(segmentData)
  .x(function(d, v) { return d.start; })
  .y(0)
  .width(function(d, v) { return d.duration; })
  .height(1)
  .margin({ top: 2, right: 0, bottom: 0, left: 4 })
  .bgColor('none')
  .color('#686868');

// In order to keep the illusion of synchronism between segments and labels,
// the labels needs to be updated when segments are modified by the user
segmentLayer.on('drag', function(item, e) {
  graph.update(labelLayer);
});

// 4. Create an anchor to visualize zooming center
// ----------------------------------------
var anchor = waves.ui.marker()
  // Set `displayHandle` to false to remove the handle of markers
  .params({ displayHandle: false })
  .color(anchorColor)
  .opacity(0.9);

// 5. Add all the components to the graph
// ----------------------------------------
graph.add(waveformLayer);
graph.add(segmentLayer);
graph.add(labelLayer);
graph.add(anchor);

// 6. draw the graph and all its components through a `d3.call` inside the `#timeline` div tag
// ----------------------------------------
d3.select('#timeline').call(graph.draw);


var zoomerSvg = d3.select('#zoomer').append('svg')
  .attr('width', graphWidth)
  .attr('height', 30);

// Create the time axis - here a common d3 axis
// Graph must be drawn in order to have `graph.xScale` up to date
var xAxis = d3.svg.axis()
  .scale(graph.xScale)
  .tickSize(1)
  .tickFormat(function(d) {
    var form = d % 1 === 0 ? '%S' : '%S:%L';
    var date = new Date(d * 1000);
    var format = d3.time.format(form);
    return format(date);
  });

// Add the axis to the newly created svg element
var axis = zoomerSvg.append('g')
  .attr('class', 'x-axis')
  .attr('transform', 'translate(0, 0)')
  .attr('fill', '#555')
  .call(xAxis);


  var zoom = zoomer()
  .select('#zoomer') // Bind the zoomer helper to the `#zoomer` tag
  .on('mousedown', function(e) {
      // Update anchor position
      var xDomainPos = graph.xScale.invert(e.anchor);
      anchor.setCurrentTime(xDomainPos);
      graph.update(anchor);
    })
    .on('mousemove', function(e) {
      // Update graph
      graph.xZoom(e);
      graph.update();
      // update axis
      axis.call(xAxis);
    })
    .on('mouseup', function(e) {
      // Set the final xZoom value of the graph
      graph.xZoomSet();
      // update axis
      axis.call(xAxis);
    });