package com.voxlearning.bigdata.MrOutput;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.lib.MultipleTextOutputFormat;

public class MultipleTextFiles extends MultipleTextOutputFormat<Text, Text> {
    /**
     * Currently, the `reducer` function in luiti use below data format.
     *     yield "", "{"json key": "json value"}"
     *  If need multiple file output, then we use the unused yield key.
     *
     * Ref code: http://blog.csdn.net/lmc_wy/article/details/7532213
     */

    protected String generateFileNameForKeyValue(Text key, Text value, String name)
    {
        String outputName = key.toString();      // Get the current filename
        key.set("");                             // We just need the value, so remove the unneeded key.
        return new Path(outputName, name).toString();   // 参考 https://github.com/klbostee/feathers
    }

}


/*
 * deploy ref: https://github.com/klbostee/feathers/blob/master/build.sh
 */
