namespace FSTutorial1 

module MyDifferentialEquations = 

    // Consider the ordinary differential equation y'=y with the initial condition y(0)=1.
    // The analytical solution is clearly y(x)=ex so using numerical methods to approximate y(1)=e is an interesting test.
    //The value e=2.718281828 is given by:
    let trueE = exp 1.0

    // Euler's method for integrating ordinary differential equations is an iterative algorithm that increments
    // the variable x by small amount dx and increments the function y(x) by dx multiplied by the gradient dy/dx.
    // This is elegantly implemented in F# as a higher-order function. The following example uses Euler's method
    // to approximate y(1)=e using one step and 100 steps, respectively:
    let euler (h: float) f (x, y) =
      x + h, y + h * f(x, y)

    // A single step
    let eulSingleStep = euler 1.0 (fun (x, y) -> y) (0.0, 1.0)

    // 100 steps
    let eulMoreSteps = Seq.unfold (fun xu -> Some(xu, euler 0.01 (fun (x, y) -> y) xu))(0.0, 1.0)
                    |> Seq.nth 100
    // Note the used of the Seq.unfold function to create an infinite on-demand sequence of 
    // results using a step size of 0.01 before extracting just the 100th element of the 
    // resulting sequence in order to approximate y(1).





    // Fourth-Order Runge-Kutta (RK4)
    let rk4 h f (x, y) =
      let k1 = h * f(x, y)
      let k2 = h * f(x + 0.5*h, y + 0.5*k1)
      let k3 = h * f(x + 0.5*h, y + 0.5*k2)
      let k4 = h * f(x + h, y + k3)
      x + h, y + k1 / 6.0 + k2 / 3.0 + k3 / 3.0 + k4 / 6.0

    // A single step
    let rkSingleStep = rk4 1.0 (fun (x, y) -> y) (0.0, 1.0)

    // 100 steps
    let rkMoreSteps = Seq.unfold (fun xu -> Some(xu, rk4 0.01 (fun (x, y) -> y) xu)) (0.0, 1.0)
                      |> Seq.nth 100







    // Partial Differential Equations
    // A partial differential equation (PDE) is an equation involving functions and their partial derivatives. 
    // Practical applications of partial differential equations include the Cauchy-Riemann equations, heat
    // conduction, the Helmholtz differential equation, Laplace's equation and the wave equation.
    // Consider transient heat conduction in a rod with the ends held at zero temperature and an initial temperature
    // profile f(x) may be expressed as the partial differential equation u_xx = u_t / c where u_xx denotes the
    // second partial derivative of u(x,t) with respect to x and u_t denotes the derivative with respect to t,
    // with the boundary conditions u(0,t)=u(1,t)=0 and the initial condition u(x,0)=1-|2x-1|.
    // The following program uses a simple algorithm known as the explicit finite difference method to compute
    // approximations to this problem:
    let solve n r f =
      let dx = 1.0 / float(n-1)
      let dt = r * dx * dx
      let g u0 u1 u2 = r*u0 + (1.0 - 2.0 * r)*u1 + r*u2
      ( 0.0,
        [|for i in 0..n-1 ->
            f(float i / float(n-1))|] )
      |> Seq.unfold (fun (t, us) ->
        Some( (t, us),
              (t + dt,
                [|yield g 0.0 us.[0] us.[1]
                  for i in 1..n-2 do
                    yield g us.[i-1] us.[i] us.[i+1]
                  yield g us.[n-2] us.[n-1] 0.0|] )))

    let testpde1 = solve 11 0.1 (fun x -> 1.0 - abs(2.0 * x - 1.0))
                   |> Seq.pick (fun (t, ux) -> if t<=0.1 then None else Some(t, ux))

    let testpde2 = solve 33 0.03 (fun x -> 1.0 - abs(2.0 * x - 1.0))
                   |> Seq.pick (fun (t, ux) -> if t<=0.1 then None else Some(t, ux))

    let testpde3 = solve 101 0.01 (fun x -> 1.0 - abs(2.0 * x - 1.0))
                   |> Seq.pick (fun (t, ux) -> if t<=0.1 then None else Some(t, ux))

    // This calculates three progressively more accurate approximations to the temperature at
    // the center of the rod after 0.1 seconds: 0.3663960707, 0.3266043218 and 0.3103926834.

    // In this case, an analytic solution may be obtained. The following code uses the analytic
    // solution to compute a much more accurate approximation to the correct answer:
    let sum i j f =
      let mutable x = 0.0
      for n in i..j do
        x <- x + f n
      x

    let u(x, t) =
      sum 1 1000000 (fun n ->
        let npi = float n * System.Math.PI
        8.0 / (npi*npi) * sin(0.5 * npi) * sin(npi * x) * exp(-npi*npi*t))

    let testfinal = u(0.5, 0.1)
