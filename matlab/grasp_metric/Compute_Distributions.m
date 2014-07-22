function [ p_c,p_n,p_nc] = Compute_Distributions(  gpModel,shapeParams,grip_point,img)
%COMPUTE_DISTRIBUTIONS Summary of this function goes here
%   Detailed explanation goes here
    
    loa = compute_loa(grip_point); 

    %Calculate Distribution Along Line 
    cov_loa = gp_cov(gpModel,loa, [], true);

    mean_loa = gp_mean(gpModel,loa,true);
   
    %Calculate Distribution Along In Workspace
    cov = gp_cov(gpModel,shapeParams.all_points,[],true); 
    mean = gp_mean(gpModel,shapeParams.all_points,true); 
    
    cov_wksp = cov(1:shapeParams.gridDim,1:shapeParams.gridDim); 
    mean_wksp = mean(1:shapeParams.gridDim); 
    
    
    %Compute Center of Mass and Plot 
%     p_com = center_of_mass(mean,cov,shapeParams.gridDim);
%     plot_com(p_com,shapeParams.com,shapeParams.gridDim,img.mean)
    
    %Compute Contact Distribution and Plot 
    p_c = contact_distribution(loa,cov_loa,mean_loa);
    plot_contact(p_c,grip_point,loa,img.mean);
    
    %Compute Normals Distribution and Plot 
   % [p_n, x] = normal_distribution(loa,cov_loa,mean_loa,p_c);
   % plot_normal(p_n,grip_point,x,img.mean)
    %plot(loa(:,1),mean_loa(1:size(loa,1)));

end

function [dist] = center_of_mass(mean,cov,gridDim)
    
    for i=1:gridDim
        for j=1:gridDim
            dist(i,j) = mvncdf(0,mean(gridDim*(i-1)+j,:),cov(gridDim*(i-1)+j,gridDim*(i-1)+j));
        end
    end

    %Normalize the grid 
    sm = 0; 
    for i=1:gridDim
        sm = sm+sum(dist(i,:)); 
    end
    
    dist = dist/sm; 
    
end



function [p] = plot_com(dist,com,gridDim,testImage)
    
    figure; 
    subplot(1,2,1)
    imshow(testImage);
 
    hold on     
    plot(2*com(:,1),2*com(:,2),'x','MarkerSize',10)
    title('Mean Function of GPIS'); 
    hold off
    
    subplot(1,2,2)
    h = surfc([1:gridDim],[1:gridDim],dist,dist); 
    %set(h,'edgecolor','interp')
    
    title('Distribution on Center of Mass'); 
    xlabel('x-axis'); 
    ylabel('y-axis'); 
    zlabel('pdf');
    
    
end

function [p] = plot_contact(dist,point,loa,testImage)
    
    figure; 
    subplot(1,2,1)
    imshow(testImage);
 
    hold on     
    plot(2*loa(:,1),2*loa(:,2))
    title('Mean Function of GPIS'); 
    hold off
    
    subplot(1,2,2)
    plot(loa(:,1),dist); 
    title('Distribution on Contact Points'); 
    xlabel('x-axis'); 
    ylabel('pdf'); 
    
    
end

function [p] = plot_normal(dist,point,x,testImage)
    
    figure; 
    subplot(1,2,1)
    imshow(testImage);
 
    hold on     
    plot(point(:,1),point(:,2))
    title('Mean Function of GPIS'); 
    axis([1,25,1,25])
    hold off
    
    subplot(1,2,2)
    h = surf(x,x,dist); 
    set(h,'edgecolor','interp')
    colormap
    title('Distribution on Surface Normals'); 
    xlabel('x-axis'); 
    ylabel('y-axis'); 
    zlabel('pdf');
    
    
end

function [loa] = compute_loa(grip_point)
%Calculate Line of Action given start and end point

    step_size = 2; 

    start_point = grip_point(1,:); 
    end_p = grip_point(2,:); 

    grad = end_p-start_point; 
    end_time = norm(grad, 2);
    grad = grad/end_time; 
    i=1; 
    time = 0;

    while(time < end_time)
        point = start_point + grad*time;
        loa(i,:) = point;
        time = time + step_size; 
        i = i + 1;
    end

end

