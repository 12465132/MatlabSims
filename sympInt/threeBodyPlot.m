function threeBodyPlot(Y, initial_conditions, markerSizes, legendNames)

    % ---- Unpack initial positions ----
    x1_0 = initial_conditions(1);  y1_0 = initial_conditions(2);
    x2_0 = initial_conditions(3);  y2_0 = initial_conditions(4);
    x3_0 = initial_conditions(5);  y3_0 = initial_conditions(6);

    % ---- Extract trajectories ----
    x1 = Y(:,1);  y1 = Y(:,2);
    x2 = Y(:,3);  y2 = Y(:,4);
    x3 = Y(:,5);  y3 = Y(:,6);

    % ---- Plot ----
    figure;
    hold on;

    % Initial markers (hidden from legend)
    plot(x1_0, y1_0, 'ro', 'MarkerFaceColor','r', 'MarkerSize',markerSizes(1), 'HandleVisibility','off');
    plot(x2_0, y2_0, 'bo', 'MarkerFaceColor','b', 'MarkerSize',markerSizes(2), 'HandleVisibility','off');
    plot(x3_0, y3_0, 'go', 'MarkerFaceColor','g', 'MarkerSize',markerSizes(3), 'HandleVisibility','off');

    % Trajectories
    plot(x1, y1, '-r', 'LineWidth',1.5, 'DisplayName',legendNames{1});
    plot(x2, y2, '-b', 'LineWidth',1.5, 'DisplayName',legendNames{2});
    plot(x3, y3, '-g', 'LineWidth',1.5, 'DisplayName',legendNames{3});

    axis equal;
    xlabel('X Position'); ylabel('Y Position');
    title('3-Body Simulation in 2D');
    set(gca,'FontSize',14);
    legend('Location','best','FontSize',20);
    grid on;
end
