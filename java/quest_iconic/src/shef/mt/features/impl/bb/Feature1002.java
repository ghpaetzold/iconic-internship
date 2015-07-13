package shef.mt.features.impl.bb;

import shef.mt.features.util.Sentence;
import java.util.HashSet;


import shef.mt.features.impl.Feature;
import shef.mt.tools.Resource;

/**
 * no tokens in target
 *
 * @author Catalina Hallett
 *
 *
 */
public class Feature1002 extends Feature {

    public Feature1002() {
        setIndex(1002);
        setDescription("no tokens in target");
        HashSet res = new HashSet<Resource>();
        setResources(res);
    }

    public void run(Sentence source, Sentence target) {
        setValue(target.getNoTokens());
    }
}
