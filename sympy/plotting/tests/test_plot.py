from sympy import (pi, sin, cos, Symbol, Integral, summation, sqrt, log,
                   oo, LambertW, I)
from sympy.plotting import (plot, plot_parametric, plot3d_parametric_line,
                            plot3d, plot3d_parametric_surface)
from sympy.plotting.plot import matplotlib, unset_show
from sympy.utilities.pytest import skip
from tempfile import NamedTemporaryFile
import warnings

unset_show()


def tmp_file(name=''):
    return NamedTemporaryFile(suffix='.png').name


def plot_and_save(name):
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    ###
    # Examples from the 'introduction' notebook
    ###

    p = plot(x)
    p = plot(x*sin(x), x*cos(x))
    p.extend(p)
    p[0].line_color = lambda a: a
    p[1].line_color = 'b'
    p.title = 'Big title'
    p.xlabel = 'the x axis'
    p[1].label = 'straight line'
    p.legend = True
    p.aspect_ratio = (1, 1)
    p.xlim = (-15, 20)
    p.save(tmp_file('%s_basic_options_and_colors.png' % name))

    p.extend(plot(x + 1))
    p.append(plot(x + 3, x**2)[1])
    p.save(tmp_file('%s_plot_extend_append.png' % name))

    p[2] = plot(x**2, (x, -2, 3))
    p.save(tmp_file('%s_plot_setitem.png' % name))

    p = plot(sin(x), (x, -2*pi, 4*pi))
    p.save(tmp_file('%s_line_explicit.png' % name))

    p = plot(sin(x))
    p.save(tmp_file('%s_line_default_range.png' % name))

    p = plot((x**2, (x, -5, 5)), (x**3, (x, -3, 3)))
    p.save(tmp_file('%s_line_multiple_range.png' % name))

    #parametric 2d plots.
    #Single plot with default range.
    plot_parametric(sin(x), cos(x)).save(tmp_file())

    #Single plot with range.
    p = plot_parametric(sin(x), cos(x), (x, -5, 5))
    p.save(tmp_file('%s_parametric_range.png' % name))

    #Multiple plots with same range.
    p = plot_parametric((sin(x), cos(x)), (x, sin(x)))
    p.save(tmp_file('%s_parametric_multiple.png' % name))

    #Multiple plots with different ranges.
    p = plot_parametric((sin(x), cos(x), (x, -3, 3)), (x, sin(x), (x, -5, 5)))
    p.save(tmp_file('%s_parametric_multiple_ranges.png' % name))

    #depth of recursion specified.
    p = plot_parametric(x, sin(x), depth=13)
    p.save(tmp_file('%s_recursion_depth' % name))

    #No adaptive sampling.
    p = plot_parametric(cos(x), sin(x), adaptive=False, nb_of_points=500)
    p.save(tmp_file('%s_adaptive' % name))

    #3d parametric plots
    p = plot3d_parametric_line(sin(x), cos(x), x)
    p.save(tmp_file('%s_3d_line.png' % name))

    p = plot3d_parametric_line(
        (sin(x), cos(x), x, (x, -5, 5)), (cos(x), sin(x), x, (x, -3, 3)))
    p.save(tmp_file('%s_3d_line_multiple' % name))

    p = plot3d_parametric_line(sin(x), cos(x), x, nb_of_points=30)
    p.save(tmp_file('%s_3d_line_points' % name))

    # 3d surface single plot.
    p = plot3d(x * y)
    p.save(tmp_file('%s_surface.png' % name))

    # Multiple 3D plots with same range.
    p = plot3d(-x * y, x * y, (x, -5, 5))
    p.save(tmp_file('%s_surface_multiple' % name))

    # Multiple 3D plots with different ranges.
    p = plot3d(
        (x * y, (x, -3, 3), (y, -3, 3)), (-x * y, (x, -3, 3), (y, -3, 3)))
    p.save(tmp_file('%s_surface_multiple_ranges' % name))

    # Single Parametric 3D plot
    p = plot3d_parametric_surface(sin(x + y), cos(x - y), x - y)
    p.save(tmp_file('%s_parametric_surface' % name))

    # Multiple Parametric 3D plots.
    p = plot3d_parametric_surface(
        (x*sin(z), x*cos(z), z, (x, -5, 5), (z, -5, 5)),
        (sin(x + y), cos(x - y), x - y, (x, -5, 5), (y, -5, 5)))
    p.save(tmp_file('%s_parametric_surface.png' % name))

    ###
    # Examples from the 'colors' notebook
    ###

    p = plot(sin(x))
    p[0].line_color = lambda a: a
    p.save(tmp_file('%s_colors_line_arity1.png' % name))

    p[0].line_color = lambda a, b: b
    p.save(tmp_file('%s_colors_line_arity2.png' % name))

    p = plot(x*sin(x), x*cos(x), (x, 0, 10))
    p[0].line_color = lambda a: a
    p.save(tmp_file('%s_colors_param_line_arity1.png' % name))

    p[0].line_color = lambda a, b: a
    p.save(tmp_file('%s_colors_param_line_arity2a.png' % name))

    p[0].line_color = lambda a, b: b
    p.save(tmp_file('%s_colors_param_line_arity2b.png' % name))

    p = plot3d_parametric_line(sin(x) + 0.1*sin(x)*cos(7*x),
             cos(x) + 0.1*cos(x)*cos(7*x),
        0.1*sin(7*x),
        (x, 0, 2*pi))
    p[0].line_color = lambda a: sin(4*a)
    p.save(tmp_file('%s_colors_3d_line_arity1.png' % name))
    p[0].line_color = lambda a, b: b
    p.save(tmp_file('%s_colors_3d_line_arity2.png' % name))
    p[0].line_color = lambda a, b, c: c
    p.save(tmp_file('%s_colors_3d_line_arity3.png' % name))

    p = plot3d(sin(x)*y, (x, 0, 6*pi), (y, -5, 5))
    p[0].surface_color = lambda a: a
    p.save(tmp_file('%s_colors_surface_arity1.png' % name))
    p[0].surface_color = lambda a, b: b
    p.save(tmp_file('%s_colors_surface_arity2.png' % name))
    p[0].surface_color = lambda a, b, c: c
    p.save(tmp_file('%s_colors_surface_arity3a.png' % name))
    p[0].surface_color = lambda a, b, c: sqrt((a - 3*pi)**2 + b**2)
    p.save(tmp_file('%s_colors_surface_arity3b.png' % name))

    p = plot3d_parametric_surface(x * cos(4 * y), x * sin(4 * y), y,
             (x, -1, 1), (y, -1, 1))
    p[0].surface_color = lambda a: a
    p.save(tmp_file('%s_colors_param_surf_arity1.png' % name))
    p[0].surface_color = lambda a, b: a*b
    p.save(tmp_file('%s_colors_param_surf_arity2.png' % name))
    p[0].surface_color = lambda a, b, c: sqrt(a**2 + b**2 + c**2)
    p.save(tmp_file('%s_colors_param_surf_arity3.png' % name))

    ###
    # Examples from the 'advanced' notebook
    ###

    i = Integral(log((sin(x)**2 + 1)*sqrt(x**2 + 1)), (x, 0, y))
    p = plot(i, (y, 1, 5))
    p.save(tmp_file('%s_advanced_integral.png' % name))

    s = summation(1/x**y, (x, 1, oo))
    p = plot(s, (y, 2, 10))
    p.save(tmp_file('%s_advanced_inf_sum.png' % name))

    p = plot(summation(1/x, (x, 1, y)), (y, 2, 10), show=False)
    p[0].only_integers = True
    p[0].steps = True
    p.save(tmp_file('%s_advanced_fin_sum.png' % name))

    ###
    # Test expressions that can not be translated to np and generate complex
    # results.
    ###
    plot(sin(x) + I*cos(x)).save(tmp_file())
    plot(sqrt(sqrt(-x))).save(tmp_file())
    plot(LambertW(x)).save(tmp_file())
    plot(sqrt(LambertW(x))).save(tmp_file())


def test_matplotlib():
    if matplotlib:
        plot_and_save('test')
    else:
        skip("Matplotlib not the default backend")
