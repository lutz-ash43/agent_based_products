barGraphIntstruction = '''

  Where data is: {
    labels: string[]
    values: {\\data: number[], label: string}[]
  }

// Examples of usage:
Each label represents a column on the x axis.
Each array in values represents a different entity. 

Here we are looking at average income for each month.
1. data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  values: [{data:[21.5, 25.0, 47.5, 64.8, 105.5, 133.2], label: 'Income'}],
}

Here we are looking at the performance of american and european players for each series. Since there are two entities, we have two arrays in values.
2. data = {
  labels: ['series A', 'series B', 'series C'],
  values: [{data:[10, 15, 20], label: 'American'}, {data:[20, 25, 30], label: 'European'}],
}
'''

horizontalBarGraphIntstruction = '''

  Where data is: {
    labels: string[]
    values: {\\data: number[], label: string}[]
  }

// Examples of usage:
Each label represents a column on the x axis.
Each array in values represents a different entity. 

Here we are looking at average income for each month.
1. data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  values: [{data:[21.5, 25.0, 47.5, 64.8, 105.5, 133.2], label: 'Income'}],
}

Here we are looking at the performance of american and european players for each series. Since there are two entities, we have two arrays in values.
2. data = {
  labels: ['series A', 'series B', 'series C'],
  values: [{data:[10, 15, 20], label: 'American'}, {data:[20, 25, 30], label: 'European'}],
}

'''


lineGraphIntstruction = '''

  Where data is: {
  xValues: number[] | string[]
  yValues: { data: number[]; label: string }[]
}

// Examples of usage:

Here we are looking at the momentum of a body as a function of mass.
1. data = {
  xValues: ['2020', '2021', '2022', '2023', '2024'],
  yValues: [
    { data: [2, 5.5, 2, 8.5, 1.5]},
  ],
}

Here we are looking at the performance of american and european players for each year. Since there are two entities, we have two arrays in yValues.
2. data = {
  xValues: ['2020', '2021', '2022', '2023', '2024'],
  yValues: [
    { data: [2, 5.5, 2, 8.5, 1.5], label: 'American' },
    { data: [2, 5.5, 2, 8.5, 1.5], label: 'European' },
  ],
}
'''

pieChartIntstruction = '''

  Where data is: {
    labels: string
    values: number
  }[]

// Example usage:
 data = [
        { id: 0, value: 10, label: 'series A' },
        { id: 1, value: 15, label: 'series B' },
        { id: 2, value: 20, label: 'series C' },
      ],
'''

scatterPlotIntstruction = '''
Where data is: {
  series: {
    data: { x: number; y: number; id: number }[]
    label: string
  }[]
}

// Examples of usage:
1. Here each data array represents the points for a different entity. 
We are looking for correlation between amount spent and quantity bought for men and women.
data = {
  series: [
    {
      data: [
        { x: 100, y: 200, id: 1 },
        { x: 120, y: 100, id: 2 },
        { x: 170, y: 300, id: 3 },
      ],
      label: 'Men',
    },
    {
      data: [
        { x: 300, y: 300, id: 1 },
        { x: 400, y: 500, id: 2 },
        { x: 200, y: 700, id: 3 },
      ],
      label: 'Women',
    }
  ],
}

2. Here we are looking for correlation between the height and weight of players.
data = {
  series: [
    {
      data: [
        { x: 180, y: 80, id: 1 },
        { x: 170, y: 70, id: 2 },
        { x: 160, y: 60, id: 3 },
      ],
      label: 'Players',
    },
  ],
}

// Note: Each object in the 'data' array represents a point on the scatter plot.
// The 'x' and 'y' values determine the position of the point, and 'id' is a unique identifier.
// Multiple series can be represented, each as an object in the outer array.
'''

boxPlotInstruction = '''

  Where data is: {
    labels: string[]
    values: {min: number, q1: number, median: number, q3: number, max: number, label: string}[]
  }

// Examples of usage:
Each label represents a group or category on the x axis.
Each object in values represents the box plot statistics for that group.

Here we are looking at the distribution of test scores for different subjects.
1. data = {
  labels: ['Math', 'Science', 'History'],
  values: [
    {min: 45, q1: 60, median: 70, q3: 80, max: 95, label: 'Math'},
    {min: 50, q1: 65, median: 75, q3: 85, max: 98, label: 'Science'},
    {min: 40, q1: 55, median: 65, q3: 75, max: 90, label: 'History'}
  ]
}

Here we are comparing the salary distributions between two departments.
2. data = {
  labels: ['Engineering', 'Marketing'],
  values: [
    {min: 55, q1: 70, median: 85, q3: 95, max: 120, label: 'Engineering'},
    {min: 40, q1: 55, median: 65, q3: 75, max: 100, label: 'Marketing'}
  ]
}

'''


graph_instructions = {
    "bar": barGraphIntstruction,
    "horizontal_bar": horizontalBarGraphIntstruction,
    "line": lineGraphIntstruction,
    "pie": pieChartIntstruction,
    "scatter": scatterPlotIntstruction,
    "box" : boxPlotInstruction
}