# coding: utf-8
import cv2
import os
import multiprocessing as mp
import feature
import utils
import stitch
import constant as const



def newPanorama(path):
    input_dirname = path
    print(input_dirname)

    pool = mp.Pool(mp.cpu_count())

    img_list, focal_length = utils.parse(input_dirname)

    # img_list = img_list[2:4]

    print('Warp images to cylinder')
    cylinder_img_list = pool.starmap(utils.cylindrical_projection, [(img_list[i], focal_length[i]) for i in range(len(img_list))])


    _, img_width, _ = img_list[0].shape
    stitched_image = cylinder_img_list[0].copy()

    shifts = [[0, 0]]
    cache_feature = [[], []]

    # add first img for end to end align
    #cylinder_img_list += [stitched_image]
    for i in range(1, len(cylinder_img_list)):
        print('Computing .... '+str(i+1)+'/'+str(len(cylinder_img_list)))
        img1 = cylinder_img_list[i-1]
        img2 = cylinder_img_list[i]

        print(' - Find features in previous img .... ', end='', flush=True)
        descriptors1, position1 = cache_feature
        if len(descriptors1) == 0:
            corner_response1 = feature.harris_corner(img1, pool)
            descriptors1, position1 = feature.extract_description(img1, corner_response1, kernel=const.DESCRIPTOR_SIZE, threshold=const.FEATURE_THRESHOLD)
        print(str(len(descriptors1))+' features extracted.')

        print(' - Find features in img_'+str(i+1)+' .... ', end='', flush=True)
        corner_response2 = feature.harris_corner(img2, pool)
        descriptors2, position2 = feature.extract_description(img2, corner_response2, kernel=const.DESCRIPTOR_SIZE, threshold=const.FEATURE_THRESHOLD)
        print(str(len(descriptors2))+' features extracted.')

        cache_feature = [descriptors2, position2]

        if const.DEBUG:
            cv2.imshow('cr1', corner_response1)
            cv2.imshow('cr2', corner_response2)
            cv2.waitKey(0)

        print(' - Feature matching .... ', end='', flush=True)
        matched_pairs = feature.matching(descriptors1, descriptors2, position1, position2, pool, y_range=const.MATCHING_Y_RANGE)
        print(str(len(matched_pairs)) +' features matched.')

        if const.DEBUG:
            utils.matched_pairs_plot(img1, img2, matched_pairs)

        print(' - Find best shift using RANSAC .... ', end='', flush=True)
        shift = stitch.RANSAC(matched_pairs, shifts[-1])
        shifts += [shift]
        print('best shift ', shift)

        print(' - Stitching image .... ', end='', flush=True)
        stitched_image = stitch.stitching(stitched_image, img2, shift, pool, blending=True)
        cwd = os.getcwd()
        data = cwd.split("\\")
        data.pop()
        source_d = '\\'.join(data)
        source_d = source_d + '\stitch'
        source_f = source_d + '\\' + str(i) + '.jpg'
        cv2.imwrite(source_f, stitched_image)
        print(str(i),'.jpg')
        print(source_d)
        print('Saved.')


    print('Perform end to end alignment')
    aligned = stitch.end2end_align(stitched_image, shifts)
    align = source_d + '\\' + 'aligned.jpg'
    cv2.imwrite(align, aligned)

    print('Cropping image')
    cropped = stitch.crop(aligned)
    cropp = source_d + '\\' + 'cropped.jpg'
    cv2.imwrite(cropp, cropped)
