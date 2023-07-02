from paraview.simple import *
import argparse
import os
from mpi4py import MPI

def view1(cam):
    cam.SetPosition(5,3,14)     # Camera position
    cam.SetFocalPoint(5,1.5,2)    # Camera focal point
    #cam.SetViewUp(0,0,-1)
    # cam.Elevation(0)
    # cam.Yaw(0)
    # cam.Roll(0)
    cam.Zoom(1.0)

def view2(cam, dz=1.0):
    cam.SetPosition(15,35,1.26)     # Camera position
    cam.SetFocalPoint(15,0,1.25)    # Camera focal point
    cam.Zoom(dz)

def view3(cam, dz=1.0):
    """ Zoom in closer in time """
    cam.SetPosition(-55,20,25)     # Camera position
    cam.SetFocalPoint(7,0.3,1.2)    # Camera focal point
    cam.Zoom(dz)

def view4(cam, t=1.0):
    """ Move away in time """
    focal_point = [7,0.3,1.2]
    end = [-55.,20.,25.]
    rmin = 0.25 # Start from half-way toward the focal point
    # r = 1: camera position == end; r = 0: camera position == focal_point
    r = rmin + (1. - rmin) * t / 600.
    cam.SetPosition(
        end[0] * r + focal_point[0] * (1. - r),
        end[1] * r + focal_point[1] * (1. - r),
        end[2] * r + focal_point[2] * (1. - r),
    )     # Camera position
    cam.SetFocalPoint(*focal_point)    # Camera focal point

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paraview animation script for the Nek5000 turbulent boundary layer DNS.')
    parser.add_argument('--data', default='flat_plate_reg.nek5000')
    parser.add_argument('--output', default='flat_plate')
    parser.add_argument('--view', type=int, default=1)
    parser.add_argument('--timestep', type=int, default=0)
    parser.add_argument('--animate', action='store_true', default=False)
    parser.add_argument('--q-criterion', action='store_true', default=False)
    parser.add_argument('--clip', action='store_true', default=False)
    parser.add_argument('--slice1', action='store_true', default=False)
    parser.add_argument('--slice2', action='store_true', default=False)
    parser.add_argument('--iso-u', action='store_true', default=False)
    parser.add_argument('--parallel', action='store_true', default=False)
  
    args = parser.parse_args()

    # Load data file
#   reader =  OpenDataFile('/Volumes/ResearchDat/nek5000/Nek5000/run/turbulent_flow_control/turbulent_boundary_layer/statistics/flat_plate.nek5000')

    if not os.path.exists(args.data):
        print('Could not locate data file')

    reader = OpenDataFile(args.data)

    reader.PointArrays = ['x_velocity','y_velocity','z_velocity']
    reader.UpdatePipeline()

    annotateTime = AnnotateTimeFilter(reader)
    Show(annotateTime)

    Render() # First render to make zoom work at the second render

    view = GetActiveView()
    cam = GetActiveCamera()

    if args.iso_u:
        """ u iso surface near the wall """

        u = 0.1    # Change u isosurface value here

        # Add coordsY to the reader
        calc = Calculator(reader)
        calc.Function = 'coordsY'
        calc.ResultArrayName = 'coordsY'
        calc.UpdatePipeline()

        # Contours
        iso_u = Contour(calc)
        iso_u.ContourBy = 'x_velocity'
        iso_u.Isosurfaces = [u]

        # Contour Coloring
        color_by = 'coordsY'
        color_range = [0., 0.1]

        arrayInfo = iso_u.PointData[color_by]
        AssignLookupTable(arrayInfo, "Cool to Warm", rangeOveride=color_range)
        dp = GetDisplayProperties(iso_u)
        dp.Representation = 'Surface'
        dp.LookupTable = GetColorTransferFunction(color_by)
        dp.ColorArrayName = color_by

        Show(iso_u)


    if args.q_criterion:
        """ Q-criterion """

        # Create Q Grid
        #q_grid_initial = FastUniformGrid()
        #q_grid_initial.WholeExtent = [0, 1000, 0, 300, 0, 400]
        #q_grid_initial.GenerateSwirlVectors = 0
        #q_grid_initial.GenerateDistanceSquaredScalars = 0
        #q_grid_initial.UpdatePipeline()
        #q_grid = Transform(q_grid_initial)
        #q_grid.Transform.Scale = [0.01, 0.01, 0.01]
        #q_grid.UpdatePipeline()

        #print('Greated Q-criterion grid')

        # Resample to q grid
        #q_grid_data = ResampleWithDataset(SourceDataArrays=reader, DestinationMesh=q_grid)

        #print('Interpolated velocity to Q-criterion grid')

        # ----- Q Criterion -----
        gradient = Gradient(reader)
        gradient.ScalarArray = 'velocity'
        gradient.ComputeGradient = 1
        gradient.ComputeQCriterion = 1
        gradient.QCriterionArrayName = 'q_criterion'

        # Contours
        contour = Contour(gradient)
        contour.ContourBy = 'q_criterion'
        contour.Isosurfaces = [1.0]

        # Contour Coloring
        color_by = 'x_velocity'
        color_range = [0, 1.0]

        arrayInfo = contour.PointData[color_by]
        AssignLookupTable(arrayInfo, "Cool to Warm", rangeOveride=color_range)
        dp = GetDisplayProperties(contour)
        dp.Representation = 'Surface'
        dp.LookupTable = GetColorTransferFunction(color_by)
        dp.ColorArrayName = color_by

        Show(contour)

    if args.slice1:
        #Resampling to a Uniform Rectilinear grid
        resampleToImage1 = ResampleToImage(Input=reader)
        # Properties modified on resampleToImage1
        resampleToImage1.UseInputBounds = 0
        resampleToImage1.SamplingDimensions = [1000, 160, 200]
        slice1 = Slice(resampleToImage1)
        slice1.SliceType = 'Plane'
        slice1.SliceType.Normal = [1,0,0]
        slice1.SliceType.Origin = [1.915,0.8,2.0]
        slice1.Triangulatetheslice = 0

        # Slice Coloring
        #color_by = 'Gradient'
        #color_range = [1, 11]

        #arrayInfo = slice1.PointData[color_by]
        #AssignLookupTable(arrayInfo, "Viridis (matplotlib)", rangeOveride=color_range)
        #dp1 = GetDisplayProperties(slice1)
        #dp1.Representation = 'Surface'
        #dp1.LookupTable = GetColorTransferFunction(color_by)
        #dp1.LookupTable.ApplyPreset('Viridis (matplotlib)', True)
        #dp1.LookupTable.RescaleTransferFunction(color_range)
        #dp1.ColorArrayName = 'du/dy'

        #s1 = Show(slice1)
        #ColorBy(s1, ('POINTS', color_by, '1'))
        #s1.SetScalarBarVisibility(view,True)

    if args.slice2:

        slice2 = Slice(reader)
        slice2.SliceType = 'Plane'
        slice2.SliceType.Normal = [1,0,0]
        slice2.SliceType.Origin = [0.01,1.5,2]

        # Slice Coloring
        color_by = 'x_velocity'
        color_range = [0, 1]

        #arrayInfo = slice2.PointData[color_by]
        #AssignLookupTable(arrayInfo, "Cool to Warm", rangeOveride=color_range)
        dp2 = GetDisplayProperties(slice2)
        dp2.Representation = 'Surface'
        #dp2.SetScalarBarVisibility(view, True)
        dp2.LookupTable = GetColorTransferFunction(color_by)
        dp2.LookupTable.ApplyPreset('Cool to Warm', True)
        dp2.LookupTable.RescaleTransferFunction(color_range)
        #dp2.ColorArrayName = color_by

        s2 = Show(slice2)
        ColorBy(s2, ('POINTS', color_by))
        s2.SetScalarBarVisibility(view,True)
    
    # Select times to animate - Split accross mpi tasks
    if args.animate:
        total_num_steps = len(reader.TimestepValues)
        if args.parallel:
            dt = total_num_steps // size + 1
    #       timestep_values = range(rank*dt,(rank+1)*dt) if rank < size-1 else range(rank*dt,total_num_steps)
            timestep_values = range(min(rank*dt,total_num_steps),min((rank+1)*dt, total_num_steps))
            print(f'rank {rank+1} of {size} will plot frames ', timestep_values)
        else:
            timestep_values = range(total_num_steps)
    else:
        timestep_values = [args.timestep]

#   timestep_values = range(len(reader.TimestepValues)) if args.animate else [args.timestep]

    # Set camera zoom before iterations
    if args.view == 2:
        min_zoom = 8.
        max_zoom = 1.
        dz = (max_zoom / min_zoom) ** (1. / (total_num_steps-1))
        if len(timestep_values) > 0:
            cam.Zoom(min_zoom * dz**timestep_values[0])
    elif args.view == 3:
        min_zoom = 2.
        max_zoom = 8.
        dz = (max_zoom / min_zoom) ** (1. / (total_num_steps-1))
        if len(timestep_values) > 0:
            cam.Zoom(min_zoom * dz**timestep_values[0])
    elif args.view == 4:
        cam.Zoom(3.)

    for timestep in timestep_values:
        print('Plotting time step ', timestep)
        view.ViewTime = reader.TimestepValues[timestep]
        view.ViewSize = [1920, 1080]

        # Camera Position
        if args.view == 1:
            view1(cam)
        elif args.view == 2:
            view2(cam, dz=dz)
        elif args.view == 3:
            view3(cam, dz=dz)
        elif args.view == 4:
            view4(cam, t=timestep)
        else:
            print('View ', args.view, ' is not available. Choosing defalut view.')
            view1(cam)

        # Render again and save
        Render()

        #SaveScreenshot(f'{args.output}_time_{timestep:06d}.png', view, ImageResolution=[4*1920, 4*1080])
        #SaveScreenshot(f'{args.output}_time_{timestep:06d}.png', view, ImageResolution=[4*1920, 4*1080],OverrideColorPalette='WhiteBackground',CompressionLevel='3')
        SaveData(f'{args.output}_{timestep:06d}.csv', proxy=slice1, ChooseArraysToWrite=1, PointDataArrays=['x_velocity', 'y_velocity', 'z_velocity'], Precision=6)


