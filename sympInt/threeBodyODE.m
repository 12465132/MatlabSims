
% Function to compute the derivatives for the 3-body problem
function dYdt = threeBodyODE(t, Y, G, m1, m2, m3, beta)
    % Unpack variables
    x1 = Y(1); y1 = Y(2);
    x2 = Y(3); y2 = Y(4);
    x3 = Y(5); y3 = Y(6);
    vx1 = Y(7); vy1 = Y(8);
    vx2 = Y(9); vy2 = Y(10);
    vx3 = Y(11); vy3 = Y(12);

    % Compute distances between bodies
    dx12 = x2 - x1; dy12 = y2 - y1; r12 = sqrt(dx12^2 + dy12^2);
    dx13 = x3 - x1; dy13 = y3 - y1; r13 = sqrt(dx13^2 + dy13^2);
    dx23 = x3 - x2; dy23 = y3 - y2; r23 = sqrt(dx23^2 + dy23^2);

    % Gravitational forces between the bodies
    F12_mag = G * m1 * m2 / r12^beta;
    F13_mag = G * m1 * m3 / r13^beta;
    F23_mag = G * m2 * m3 / r23^beta;

    theta12 = atan2(dy12, dx12); % Angle between the two bodies
    theta13 = atan2(dy13, dx13); % Angle between the two bodies
    theta23 = atan2(dy23, dx23); % Angle between the two bodies

    % Decompose forces into x and y components
    F12_x = F12_mag * cos(theta12); F12_y = F12_mag * sin(theta12);
    F13_x = F13_mag * cos(theta13); F13_y = F13_mag * sin(theta13);
    F23_x = F23_mag * cos(theta23); F23_y = F23_mag * sin(theta23);

    % Accelerations for each body
    ax1 = (F12_x + F13_x) / m1;
    ay1 = (F12_y + F13_y) / m1;
    ax2 = (-F12_x + F23_x) / m2;
    ay2 = (-F12_y + F23_y) / m2;
    ax3 = (-F13_x - F23_x) / m3;
    ay3 = (-F13_y - F23_y) / m3;

    % Pack derivatives into a column vector
    dYdt = [vx1; vy1; vx2; vy2; vx3; vy3; ax1; ay1; ax2; ay2; ax3; ay3];
end
