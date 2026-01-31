function threeBodyAnimation(Y, speed, markerSizes, legendNames, showLines)

    if nargin < 5 || isempty(showLines)
        showLines = false;             % default: markers only
    end

    % ---- Extract positions ----
    x1 = Y(:,1);  y1 = Y(:,2);
    x2 = Y(:,3);  y2 = Y(:,4);
    x3 = Y(:,5);  y3 = Y(:,6);

    % ---- Figure ----
    figure; hold on;

    % Trajectory lines (only if showLines==true)
    if showLines
        plot(x1, y1, '-r', 'LineWidth',1.5, 'DisplayName',legendNames{1});
        plot(x2, y2, '-b', 'LineWidth',1.5, 'DisplayName',legendNames{2});
        plot(x3, y3, '-g', 'LineWidth',1.5, 'DisplayName',legendNames{3});
    end

    % Axis limits with symmetric margin (fixed during animation)
    xs = [x1; x2; x3];  ys = [y1; y2; y3];
    xc = mean([min(xs) max(xs)]);  yc = mean([min(ys) max(ys)]);
    halfSpan = 0.5*max( [max(xs)-min(xs),  max(ys)-min(ys)] );
    R = 1.05*halfSpan;   % 5% margin
    
    xlim([xc-R, xc+R]);
    ylim([yc-R, yc+R]);
    
    % --- Freeze limits & keep square pixels without touching limits ---
    set(gca,'XLimMode','manual','YLimMode','manual');  % hard lock
    axis manual                                          % belt & suspenders
    daspect([1 1 1]);                                    

    xlabel('X Position'); ylabel('Y Position');
    title('3-Body Simulation in 2D');
    set(gca,'FontSize',14); grid on;

    % Markers: in legend only when showLines==false
    hv = 'on';                         % markers visible in legend by default
    if showLines, hv = 'off'; end      % hide marker handles if lines are shown

    h1 = plot(x1(1), y1(1), 'or', 'MarkerFaceColor','r', ...
              'MarkerSize',markerSizes(1), 'HandleVisibility',hv, ...
              'DisplayName',legendNames{1});
    h2 = plot(x2(1), y2(1), 'ob', 'MarkerFaceColor','b', ...
              'MarkerSize',markerSizes(2), 'HandleVisibility',hv, ...
              'DisplayName',legendNames{2});
    h3 = plot(x3(1), y3(1), 'og', 'MarkerFaceColor','g', ...
              'MarkerSize',markerSizes(3), 'HandleVisibility',hv, ...
              'DisplayName',legendNames{3});

    L = legend('Location','northeast','FontSize',15);  % create once
    L.AutoUpdate = 'off';


    % --- before loop ---
    axis manual; daspect([1 1 1]);
    targetFPS = 60 * speed;          % speed=2 doubles playback; 0.5 halves it
    dt = 1 / targetFPS;
    
    % optional frame skipping if N is huge (also scaled by speed)
    baseFrames = 1500;
    step = max(1, floor(size(Y,1) / (baseFrames * speed)));
    
    tprev = tic;
    for i = 1:step:size(Y,1)
        set(h1,'XData',x1(i),'YData',y1(i));
        set(h2,'XData',x2(i),'YData',y2(i));
        set(h3,'XData',x3(i),'YData',y3(i));
        drawnow limitrate nocallbacks
        t = toc(tprev);
        if t < dt, pause(dt - t); end
        tprev = tic;
    end


end
