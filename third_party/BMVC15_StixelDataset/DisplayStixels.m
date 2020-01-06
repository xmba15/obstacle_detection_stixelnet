function DisplayStixels (gt_filename, images_base_dir)


if exist(gt_filename, 'file') == 0
    str = sprintf('could not file file %s', stixels_db_dir);
    disp(str);
    return;
end

fid = fopen(gt_filename,'r');

prev_series_id = -1;
prev_frame_id = -1;
prev_date_str = '';

max_points_per_frame = 300;
num_points_cur_frame = 0;

points_cur_frame = zeros(max_points_per_frame, 2);
while ~feof(fid)
    dateStr = fscanf(fid,'%s',1);
    series_id = fscanf(fid,'%d',1);
    frame_id = fscanf(fid,'%d',1);
    x_pos = fscanf(fid,'%d',1);
    y_pos = fscanf(fid,'%d',1);
    data_type = fscanf(fid,'%s',1); % Train / Test

    num_points_cur_frame = num_points_cur_frame+1;
    points_cur_frame(num_points_cur_frame, 1) = x_pos;
    points_cur_frame(num_points_cur_frame, 2) = y_pos;

    if prev_frame_id > 0 && (frame_id ~= prev_frame_id || series_id ~= prev_series_id)
        % image_filename = sprintf('%s\\2011_%s\\2011_%s_drive_%04d_sync\\image_02\\data\\%010d.png', images_base_dir, prev_date_str, prev_date_str, prev_series_id, prev_frame_id);
        image_filename = sprintf('%s/2011_%s/2011_%s_drive_%04d_sync/image_02/data/%010d.png', images_base_dir, prev_date_str, prev_date_str, prev_series_id, prev_frame_id);
        if exist(image_filename, 'file') == 0
            str = sprintf('could not find image file %s', image_filename);
            disp(str);
        else
            imshow(image_filename);
            hold on
            plot(points_cur_frame(1:num_points_cur_frame,1), points_cur_frame(1:num_points_cur_frame,2), 'm.');
            pause
            hold off
            num_points_cur_frame = 0;
        end
    end
    prev_frame_id = frame_id;
    prev_series_id = series_id;
    prev_date_str = dateStr;
end
